# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bgpneiget']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'junos-eznc>=2.6.3,<3.0.0', 'napalm>=3.3.1,<4.0.0']

entry_points = \
{'console_scripts': ['bgpneiget = bgpneiget.cli:cli']}

setup_kwargs = {
    'name': 'bgpneiget',
    'version': '1.0.2',
    'description': 'Get BGP Neighbours from network devices',
    'long_description': '# bgpneiget\n\nGet BGP neighbours from network devices and output a json\nobject.\n\n# Configuration\n\nCreate a config file in ~/.config/bgpneiget/config.json\n\n```json\n{\n    "username": "user",\n    "password": "password"\n}\n```\n\n# Usage\n\nRun the command with --help to see command line options.\n',
    'author': 'Rob Woodward',
    'author_email': 'rob@emailplus.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/robwdwd/bgpneiget',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
