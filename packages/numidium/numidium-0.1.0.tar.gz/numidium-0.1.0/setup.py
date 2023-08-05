# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numidium']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'numidium',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Greatness7',
    'author_email': 'Greatness7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
