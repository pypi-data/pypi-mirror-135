from arc import CLI, State, errors, Context
from arc.color import colorize, fg
from i3ipc import Connection


class MagicState(State):
    wm: Connection


cli = CLI("magic-window", state={"wm": Connection()})

MARK = "__magic_window"


def get_magic_container(wm: Connection):
    marked = wm.get_tree().find_marked(MARK)

    if len(marked) > 1:
        raise errors.ExecutionError(
            f"Multiple magic windows, run {colorize('magic-window clear', fg.YELLOW)}"
        )
    if len(marked) == 0:
        raise errors.ExecutionError(
            f"No magic window found. Use {colorize('magic-window pick', fg.YELLOW)} "
            "to pick the currently focused one"
        )

    return marked[0]


def remove_marks(wm: Connection):
    for marked in wm.get_tree().find_marked(MARK):
        print(f"({marked.id}) {marked.name} is no longer a magic window")
        marked.command(f"unmark {MARK}")


@cli.command()
def pick(state: MagicState):
    """Sets the currently focused container as the magic window"""
    remove_marks(state.wm)

    focused = state.wm.get_tree().find_focused()
    if not focused:
        raise errors.ExecutionError("No focused window")

    focused.command(f"mark --add {MARK}")
    print(f"({focused.id}) {focused.name} is now the magic window")


@cli.command()
def show(state: MagicState):
    """Shows the magic window"""
    magic = get_magic_container(state.wm)

    workspace = state.wm.get_tree().find_focused().workspace()
    magic.command(f"move container to workspace {workspace.name}")
    magic.command("focus")


@cli.command()
def hide(state: MagicState):
    """Hides the magic window"""
    magic = get_magic_container(state.wm)
    magic.command("move scratchpad")


@cli.command()
def clear(state: MagicState):
    """Removes all magic windows"""
    remove_marks(state.wm)


@cli.command()
def which(state: MagicState):
    """Prints out information about the current magic window"""
    magic = get_magic_container(state.wm)
    print(f"({magic.id}) {magic.name}")


@cli.command()
def toggle(ctx: Context, state: MagicState):
    """Toggles the magic window"""
    magic = get_magic_container(state.wm)
    if magic.focused:
        ctx.execute(hide)
    else:
        ctx.execute(show)


if __name__ == "__main__":
    cli()
