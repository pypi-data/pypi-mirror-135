# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylinearalg']

package_data = \
{'': ['*']}

install_requires = \
['sympy>=1.9,<2.0']

setup_kwargs = {
    'name': 'pylinearalg',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Thomas Breydo',
    'author_email': 'tbreydo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
