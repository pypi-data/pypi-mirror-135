# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xkcd_cli_viewer', 'xkcd_cli_viewer.cli']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=11.0.0,<12.0.0',
 'thefuzz[speedup]>=0.19.0,<0.20.0']

entry_points = \
{'console_scripts': ['xkcd-cli = xkcd_cli_viewer.cli.main:main']}

setup_kwargs = {
    'name': 'xkcd-cli-viewer',
    'version': '0.1.2',
    'description': 'A CLI that scrapes the XKCD website.',
    'long_description': None,
    'author': 'iamkneel',
    'author_email': 'nsdj.sharma@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
