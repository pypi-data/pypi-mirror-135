# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rss_reader',
 'rss_reader.argument_parser',
 'rss_reader.config',
 'rss_reader.converter',
 'rss_reader.imports',
 'rss_reader.printer',
 'rss_reader.reader']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2',
 'colorama>=0.4.3,<0.5.0',
 'ebooklib>=0.17.1,<0.18.0',
 'pathvalidate>=2.4.1,<3.0.0',
 'pydantic',
 'requests',
 'rss-parser>=0.2.3,<0.3.0',
 'weasyprint>=51,<52']

entry_points = \
{'console_scripts': ['rss-reader = rss_reader.__main__:main']}

setup_kwargs = {
    'name': 'rss-reader',
    'version': '3.5.1',
    'description': 'A simple CLI rss reader',
    'long_description': "# Rss reader\n\n[![Downloads](https://pepy.tech/badge/rss-reader)](https://pepy.tech/project/rss-reader)\n[![Downloads](https://pepy.tech/badge/rss-reader/month)](https://pepy.tech/project/rss-reader/month)\n[![Downloads](https://pepy.tech/badge/rss-reader/week)](https://pepy.tech/project/rss-reader/week)\n\n[![PyPI version](https://img.shields.io/pypi/v/rss-reader)](https://pypi.org/project/rss-reader)\n[![Python versions](https://img.shields.io/pypi/pyversions/rss-reader)](https://pypi.org/project/rss-reader)\n[![Wheel status](https://img.shields.io/pypi/wheel/rss-reader)](https://pypi.org/project/rss-reader)\n[![License](https://img.shields.io/pypi/l/rss-reader?color=success)](https://github.com/dhvcc/rss-reader/blob/master/LICENSE)\n[![GitHub Pages](https://badgen.net/github/status/dhvcc/rss-reader/gh-pages?label=docs)](https://dhvcc.github.io/rss-reader#documentation)\n\n[![Code checks](https://github.com/dhvcc/rss-reader/workflows/Code%20checks/badge.svg)](https://github.com/dhvcc/rss-reader/actions?query=workflow%3A%22Code+checks%22)\n[![Pypi publish](https://github.com/dhvcc/rss-reader/workflows/Pypi%20publish/badge.svg)](https://github.com/dhvcc/rss-reader/actions?query=workflow%3A%22Pypi+publish%22)\n\n## What is this?\n\n`rss-reader` is a command line utility that allows you to view RSS feeds\n\nYou can also convert RSS feeds to `html`/`pdf`/`epub` for more convenient reading\n\nCommand-line arguments, local and global INI configs, environment variables **are supported**\n\n## What is RSS?\n\nRSS stands for “Really Simple Syndication,”\nor, depending on who you ask, “Rich Site Summary.” At it's heart, RSS is\njust simple text files with basic updated information—news pieces,\narticles, that sort of thing. That stripped-down content is usually\nplugged into what is called a “feed reader” or an interface that quickly\nconverts the RSS text files into a stream of the latest updates from\naround the web.\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first\nto discuss what you would like to change.\n\nInstall dependencies with `poetry install` (`pip install poetry`)\n\n`pre-commit` usage is highly recommended. To install hooks run\n\n```bash\npoetry run pre-commit install -t=pre-commit -t=pre-push\n```\n\n## License\n\n[GPLv3](https://github.com/dhvcc/rss-reader/blob/master/LICENSE)\n",
    'author': 'dhvcc',
    'author_email': '1337kwiz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
