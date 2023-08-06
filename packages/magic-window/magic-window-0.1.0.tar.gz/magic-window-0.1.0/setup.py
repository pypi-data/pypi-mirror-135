# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magic_window']

package_data = \
{'': ['*'],
 'magic_window': ['stubs/i3ipc/*',
                  'stubs/i3ipc/_private/*',
                  'stubs/i3ipc/aio/*']}

install_requires = \
['arc-cli>=6.2.2,<7.0.0', 'i3ipc>=2.2.1,<3.0.0']

entry_points = \
{'console_scripts': ['magic-window = magic_window.__main__:cli']}

setup_kwargs = {
    'name': 'magic-window',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Sean Collings',
    'author_email': 'seanrcollings@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
