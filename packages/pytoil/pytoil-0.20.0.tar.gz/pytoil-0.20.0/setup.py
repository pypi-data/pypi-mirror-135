# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytoil',
 'pytoil.api',
 'pytoil.cli',
 'pytoil.config',
 'pytoil.environments',
 'pytoil.git',
 'pytoil.repo',
 'pytoil.starters',
 'pytoil.vscode']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==6.0',
 'aiofiles==0.8.0',
 'anyio==3.5.0',
 'asyncclick==8.0.3.2',
 'cookiecutter==1.7.3',
 'httpx[http2]==0.21.3',
 'humanize==3.13.1',
 'pydantic==1.9.0',
 'rich==11.0.0',
 'thefuzz[speedup]==0.19.0',
 'tomlkit==0.8.0',
 'virtualenv==20.13.0',
 'wasabi==0.9.0']

entry_points = \
{'console_scripts': ['pytoil = pytoil.cli.root:main']}

setup_kwargs = {
    'name': 'pytoil',
    'version': '0.20.0',
    'description': 'CLI to automate the development workflow.',
    'long_description': "![logo](https://github.com/FollowTheProcess/pytoil/raw/main/docs/img/logo.png)\n\n[![License](https://img.shields.io/github/license/FollowTheProcess/pytoil)](https://github.com/FollowTheProcess/pytoil)\n[![PyPI](https://img.shields.io/pypi/v/pytoil.svg?logo=python)](https://pypi.python.org/pypi/pytoil)\n[![GitHub](https://img.shields.io/github/v/release/FollowTheProcess/pytoil?logo=github&sort=semver)](https://github.com/FollowTheProcess/pytoil)\n[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/FollowTheProcess/pytoil)\n[![CI](https://github.com/FollowTheProcess/pytoil/workflows/CI/badge.svg)](https://github.com/FollowTheProcess/pytoil/actions?query=workflow%3ACI)\n[![Coverage](https://github.com/FollowTheProcess/pytoil/raw/main/docs/img/coverage.svg)](https://github.com/FollowTheProcess/pytoil)\n\n*pytoil is a small, helpful CLI to help developers manage their local and remote projects with ease!*\n\n* **Source Code**: [https://github.com/FollowTheProcess/pytoil](https://github.com/FollowTheProcess/pytoil)\n\n* **Documentation**: [https://FollowTheProcess.github.io/pytoil/](https://FollowTheProcess.github.io/pytoil/)\n\n## What is it?\n\n`pytoil` is a handy tool that helps you stay on top of all your projects, remote or local. It's primarily aimed at python developers but you could easily use it to manage any project!\n\npytoil is:\n\n* Easy to use ✅\n* Easy to configure ✅\n* Safe (it won't edit your repos at all) ✅\n* Snappy (it's asynchronous from the ground up and as much as possible is done concurrently, clone all your repos in seconds!) 💨\n* Useful! (I hope 😃)\n\nSay goodbye to janky bash scripts 👋🏻\n\n## Installation\n\nAs pytoil is a CLI, I recommend [pipx]\n\n```shell\npipx install pytoil\n```\n\nOr just pip (but must be globally available)\n\n```shell\npip install pytoil\n```\n\n## Quickstart\n\n`pytoil` is super easy to get started with.\n\nAfter installation just run\n\n```shell\n$ pytoil config\n\nNo config file yet!\nMaking you a default one...\n```\n\nThis will create a default config file which can be found at `~/.pytoil.yml`. See the [docs] for what information you need to put in here.\n\nDon't worry though, there's only a few options to configure! 😴\n\nAfter that you're good to go! You can do things like:\n\n#### See your local and remote projects\n\n```shell\npytoil show all\n```\n\n#### See which ones you have on GitHub, but not on your computer\n\n```shell\npytoil show diff\n```\n\n#### Easily grab a project, regardless of where it is\n\n```shell\npytoil checkout my_project\n```\n\n#### Create a new project and virtual environment in one go\n\n```shell\npytoil new my_project --venv venv\n\n```\n\n#### And even do this from a [cookiecutter] template\n\n```shell\npytoil new my_project --venv venv --cookie https://github.com/some/cookie.git\n```\n\nCheck out the [docs] for more 💥\n\n## Contributing\n\n`pytoil` is an open source project and, as such, welcomes contributions of all kinds 😃\n\nYour best bet is to check out the [contributing guide] in the docs!\n\n### Credits\n\nThis package was created with [cookiecutter] and the [FollowTheProcess/poetry_pypackage] project template.\n\n`pytoil` has been built on top of these fantastic projects:\n\n* [async-click]\n* [cookiecutter]\n* [wasabi]\n* [httpx]\n\n[pipx]: https://pipxproject.github.io/pipx/\n[cookiecutter]: https://cookiecutter.readthedocs.io/en/1.7.2/\n[docs]: https://FollowTheProcess.github.io/pytoil/\n[FollowTheProcess/poetry_pypackage]: https://github.com/FollowTheProcess/poetry_pypackage\n[wasabi]: https://github.com/ines/wasabi\n[httpx]: https://www.python-httpx.org\n[async-click]: https://github.com/python-trio/asyncclick\n[contributing guide]: https://followtheprocess.github.io/pytoil/contributing/contributing.html\n",
    'author': 'Tom Fleet',
    'author_email': 'tomfleet2018@gmail.com',
    'maintainer': 'Tom Fleet',
    'maintainer_email': 'tomfleet2018@gmail.com',
    'url': 'https://github.com/FollowTheProcess/pytoil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
