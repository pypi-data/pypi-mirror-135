# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylinearalg']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pylinearalg',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Thomas Breydo',
    'author_email': 'tbreydo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
