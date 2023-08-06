# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastack', 'fastack.middleware']

package_data = \
{'': ['*']}

install_requires = \
['Werkzeug>=2.0.2,<3.0.0',
 'asgi-lifespan>=1.0.1,<2.0.0',
 'cookiecutter>=1.7.3,<2.0.0',
 'fastapi>=0.72.0,<0.73.0',
 'typer>=0.4.0,<0.5.0',
 'uvicorn[standard]>=0.16.0,<0.17.0']

entry_points = \
{'console_scripts': ['fastack = fastack.__main__:fastack']}

setup_kwargs = {
    'name': 'fastack',
    'version': '4.0.0',
    'description': 'fastack is an intuitive framework based on FastAPI',
    'long_description': '# Fastack\n\n<p align="center">\n<a href="https://github.com/fastack-dev/fastack"><img src="https://raw.githubusercontent.com/fastack-dev/fastack/main/docs/images/logo.png" alt="Fastack"></a>\n</p>\n<p align="center">\n    <em>⚡ Fastack makes your FastAPI much easier 😎</em>\n</p>\n<p align="center">\n<img alt="PyPI" src="https://img.shields.io/pypi/v/fastack?color=%23d3de37">\n<img alt="PyPI - Status" src="https://img.shields.io/pypi/status/fastack">\n<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/fastack?style=flat">\n<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/fastack?style=flat">\n<img alt="PyPI - License" src="https://img.shields.io/pypi/l/fastack?color=%2328a682">\n<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n<a href="https://results.pre-commit.ci/latest/github/fastack-dev/fastack/main"><img src="https://results.pre-commit.ci/badge/github/fastack-dev/fastack/main.svg"></a>\n<a href="https://codecov.io/gh/fastack-dev/fastack">\n<img src="https://codecov.io/gh/fastack-dev/fastack/branch/main/graph/badge.svg?token=01EBPHVTKX"/>\n</a>\n</p>\n\nfastack is an intuitive framework based on FastAPI, for creating clean and easy-to-manage REST API project structures. It\'s built for FastAPI framework ❤️\n\n## WARNING 🚨\n\nThis is an early development, lots of changes with each release. Also this is an experimental project, as I\'m currently studying asynchronous environments.\n\nFYI, this isn\'t the only intuitive framework project I\'ve made. I\'ve also made with different framework bases, including:\n\n* [zemfrog](https://github.com/zemfrog/zemfrog) - Based on [Flask framework](https://flask.palletsprojects.com)\n* [falca](https://github.com/aprilahijriyan/falca) - Based on [Falcon framework](https://falconframework.org/)\n\n\n\n## Features 🔥\n\n* Project layout (based on cookiecutter template)\n* Pagination support\n* Provide a `Controller` class for creating REST APIs\n* Provides command line to manage app\n* Support to access `app`, `request`, `state`, and `websocket` globally!\n* and more!\n\n## Plugins 🎉\n\nList of official plugins:\n\n* [fastack-sqlmodel](https://github.com/fastack-dev/fastack-sqlmodel) - [SQLModel](https://github.com/tiangolo/sqlmodel) integration for fastack.\n* [fastack-migrate](https://github.com/fastack-dev/fastack-migrate) - [Alembic](https://alembic.sqlalchemy.org/en/latest/) integration for fastack.\n* [fastack-mongoengine](https://github.com/fastack-dev/fastack-mongoengine) - [MongoEngine](https://github.com/MongoEngine/mongoengine) integration for fastack.\n* [fastack-cache](https://github.com/fastack-dev/fastack-cache) - Caching plugin for fastack\n\n## Installation 📦\n\n```\npip install -U fastack\n```\n\n## Example 📚\n\nCreate a project\n\n```\nfastack new awesome-project\ncd awesome-project\n```\n\nInstall pipenv & create virtual environment\n\n```\npip install pipenv && pipenv install && pipenv shell\n```\n\nRun app\n\n```\nfastack runserver\n```\n\n## Documentation 📖\n\nFor the latest documentation, see the [feature/docs](https://github.com/fastack-dev/fastack/tree/feature/docs) branch.\n\nBuild the latest documentation locally:\n\n```\nmkdocs serve\n```\n\nOr alternatively, you can visit https://fastack.readthedocs.io/en/latest/\n\n## Tests 🔬\n\nRun tests with ``tox``, maybe you need to install python version `3.7`, `3.8` and `3.9` first.\n\n```\ntox\n```\n\nAll components have not been fully tested, feel free if anyone wants to help make unit tests :)\n',
    'author': 'aprilahijriyan',
    'author_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'maintainer': 'aprilahijriyan',
    'maintainer_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'url': 'https://github.com/fastack-dev/fastack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
