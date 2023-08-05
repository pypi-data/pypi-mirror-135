# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyobs_alpaca']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26,<3.0']

setup_kwargs = {
    'name': 'pyobs-alpaca',
    'version': '0.16.1',
    'description': 'pyobs module for ASCOM Alpaca',
    'long_description': None,
    'author': 'Tim-Oliver Husser',
    'author_email': 'thusser@uni-goettingen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
