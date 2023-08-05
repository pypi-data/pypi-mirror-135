# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdrf', 'gdrf.infer', 'gdrf.models', 'gdrf.utils', 'gdrf.visualize', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0',
 'gpytorch>=1.5.0,<2.0.0',
 'holoviews>=1.14.6,<2.0.0',
 'hvplot>=0.7.3,<0.8.0',
 'matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.21.0,<2.0.0',
 'pandas<1.3.0',
 'pillow>=8.3.2,<9.0.0',
 'plotly>=5.2.2,<6.0.0',
 'pyro-ppl>=1.6.0,<2.0.0',
 'pyyaml>=5.4.0,<6.0.0',
 'scipy>=1.7.0,<2.0.0',
 'torch>=1.9.0,<2.0.0',
 'torchvision>=0.10.0,<0.11.0',
 'tqdm>=4.61.1,<5.0.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'poetry>=1.1.10,<2.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['wandb>=0.12.0,<0.13.0',
         'mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.15.2,<0.16.0',
         'mkdocs-autorefs==0.1.1'],
 'test': ['black>=20.8b1,<21.0',
          'isort>=5.6.4,<6.0.0',
          'flake8>=3.8.4,<4.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest>=6.1.2,<7.0.0',
          'pytest-cov>=2.10.1,<3.0.0']}

entry_points = \
{'console_scripts': ['gdrf = gdrf.cli:main']}

setup_kwargs = {
    'name': 'gdrf',
    'version': '0.1.3',
    'description': 'Pytorch+GPytorch implementation of GDRFs from San Soucie et al. 2020.',
    'long_description': '# Gaussian-Dirichlet Random Fields\n\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/gdrf">\n    <img src="https://img.shields.io/pypi/v/gdrf.svg"\n        alt = "Release Status">\n</a>\n\n<a href="https://github.com/san-soucie/gdrf/actions">\n    <img src="https://github.com/san-soucie/gdrf/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">\n</a>\n\n<a href="https://gdrf.readthedocs.io/en/latest/?badge=latest">\n    <img src="https://readthedocs.org/projects/gdrf/badge/?version=latest" alt="Documentation Status">\n</a>\n\n</p>\n\n\nPytorch+GPytorch implementation of GDRFs from San Soucie et al. 2020\n\n\n* Free software: MIT\n* Documentation: <https://gdrf.readthedocs.io>\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.\n',
    'author': 'John San Soucie',
    'author_email': 'jsansoucie@whoi.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/san-soucie/gdrf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<3.10',
}


setup(**setup_kwargs)
