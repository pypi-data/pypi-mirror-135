# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['migu_music_dl']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'prettytable>=3.0.0,<4.0.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['migu-music-dl = migu_music_dl.cli: download']}

setup_kwargs = {
    'name': 'migu-music-dl',
    'version': '0.1.2',
    'description': 'Migu music downloader',
    'long_description': '\n# MIGU-Music-dl   \n\n[![PyPI version](https://badge.fury.io/py/migu-music-dl.svg)](https://badge.fury.io/py/migu-music-dl)\n[![Publish Action](https://github.com/swim2sun/migu-music-dl/actions/workflows/publish.yml/badge.svg)](https://github.com/swim2sun/migu-music-dl/actions/workflows/publish.yml)\n\nDownload Migu Lossless Music\n\n## Installation\n\n### Install from PyPI\n\n```shell\n$ pip install migu-music-dl\n```\n\n### Install from Homebrew\n```shell\n$ brew tap swim2sun/migu-music-dl\n$ brew install migu-music-dl\n```\n    \n\nUsage\n-----\n\n```shell\n$ migu-music-dl [OPTIONS] SEARCH_KEYWORD OUTPUT_DIR\n```\n\n![terminal](./screenshot.png)',
    'author': 'swim2sun',
    'author_email': 'xiangyangyou@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/swim2sun/migu-music-dl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
