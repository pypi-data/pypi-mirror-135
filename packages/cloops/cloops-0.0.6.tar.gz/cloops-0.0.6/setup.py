# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloops', 'cloops.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cloops',
    'version': '0.0.6',
    'description': 'dfdfgdfg',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
