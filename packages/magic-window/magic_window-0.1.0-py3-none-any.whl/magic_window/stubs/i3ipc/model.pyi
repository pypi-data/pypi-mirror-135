class Rect:
    x: int
    y: int
    height: int
    width: int
    def __init__(self, data: dict) -> None: ...

class OutputMode:
    width: int
    height: int
    refresh: bool
    def __init__(self, data: dict) -> None: ...
    def __getitem__(self, item: str): ...

class Gaps:
    inner: int
    outer: int
    left: int
    right: int
    top: int
    bottom: int
    def __init__(self, data: dict) -> None: ...
