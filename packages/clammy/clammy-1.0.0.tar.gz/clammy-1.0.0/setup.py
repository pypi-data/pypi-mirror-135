# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clammy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'clammy',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'ranguli',
    'author_email': 'hello@joshmurphy.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
