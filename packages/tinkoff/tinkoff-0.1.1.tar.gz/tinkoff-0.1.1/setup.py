# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinkoff']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tinkoff',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Danil Akhtarov',
    'author_email': 'd.akhtarov@tinkoff.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
