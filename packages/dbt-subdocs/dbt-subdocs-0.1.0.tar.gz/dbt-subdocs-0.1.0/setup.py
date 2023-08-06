# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt_subdocs', 'dbt_subdocs.usecase']

package_data = \
{'': ['*']}

install_requires = \
['dbt-core>=1.0.1,<2.0.0', 'rich>=10.14.0,<11.0.0', 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['dbt-subdocs = dbt_subdocs.__main__:app']}

setup_kwargs = {
    'name': 'dbt-subdocs',
    'version': '0.1.0',
    'description': 'dbt-subdocs is a python CLI you can used to generate a dbt-docs for a subset of your dbt project',
    'long_description': '# dbt-subdocs\n\n<div align="center">\n\n[![Build status](https://github.com/jb-delafosse/dbt-subdocs/workflows/build/badge.svg?branch=master&event=push)](https://github.com/jb-delafosse/dbt-subdocs/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/dbt-subdocs.svg)](https://pypi.org/project/dbt-subdocs/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/jb-delafosse/dbt-subdocs/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/jb-delafosse/dbt-subdocs/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/jb-delafosse/dbt-subdocs/releases)\n[![License](https://img.shields.io/github/license/jb-delafosse/dbt-subdocs)](https://github.com/jb-delafosse/dbt-subdocs/blob/master/LICENSE)\n![Coverage Report](assets/images/coverage.svg)\n\ndbt-subdocs is a python CLI you can used to generate a dbt-docs for a subset of your dbt project\n\n</div>\n\n## 🤔 Description\n\nThis project is useful if you want to generate a dbt-docs site for a subset of the models in your DBT project.\nBy default, in dbt-docs, all your projects gets documented : \n- all the models\n- all the sources\n- all the tests\n- and all the macros\n\nThis CLI is useful if you only want to document what your end-user will be using.\n\nThis CLI simply edits the `manifest.json` and `catalog.json` used by the dbt-docs site so they do not\ncontain nodes you don\'t want to display.\n\n## ✨ Features\n\n- Configure an input and output directory\n- Select the models to document using tag within DBT\n- Choose to exclude nodes that are useless for your users : tests, macros, seed etc...\n\n## 🏃 Getting Started\n\n\n<details>\n  <summary>Installation with pip</summary>\n\n```bash\npip install -U dbt-subdocs\n```\n\nThen you can run\n\n```bash\ndbt-subdocs --help\n```\n</details>\n\n<details>\n  <summary>First call to the CLI</summary>\n\n  You can call dbt-subdocs by simply using the command `dbt-subdocs`\n  See all the options available using `dbt-subdocs --help`\n</details>\n\n<details>\n  <summary>Usecase 1: Only display nodes with a specific tag</summary>\n\n  Assuming your `manifest.json` and `catalog.json` are in `DIRECTORY`, simply call\n  ```bash\n  cd DIRECTORY\n  dbt-subdocs --tag finance\n  ```\n\n  If you want to select nodes with tags `finance` OR `engineering`, simply call\n  ```bash\n  dbt-subdocs --tag finance --tag engineering\n  ```\n</details>\n\n<details>\n  <summary>Usecase 2: Removing macros from the docs</summary>\n\n  If you want to remove macros from the `manifest.json` you can call \n  ```bash\n  dbt-subdocs --tag finance --exclude-node-type macros\n  ```\n  You can also remove sources by using \n  ```bash\n  dbt-subdocs --tag finance --exclude-node-type macros --exclude-node-type sources\n  ```\n</details>\n\n## 🛡️ License\n\n[![License](https://img.shields.io/github/license/jb-delafosse/dbt-subdocs)](https://github.com/jb-delafosse/dbt-subdocs/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/jb-delafosse/dbt-subdocs/blob/master/LICENSE) for more details.\n\n## 📃 Citation\n\n```bibtex\n@misc{dbt-subdocs,\n  author = {jb-delafosse},\n  title = {dbt-subdocs is a python CLI you can used to generate a dbt-docs for a subset of your dbt project},\n  year = {2022},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/jb-delafosse/dbt-subdocs}}\n}\n```\n\n## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)\n',
    'author': 'jb-delafosse',
    'author_email': 'hello@jb-delafosse.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jb_delafosse/dbt-subdocs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
