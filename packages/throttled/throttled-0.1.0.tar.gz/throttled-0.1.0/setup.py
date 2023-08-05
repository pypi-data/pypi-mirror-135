# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['throttled']

package_data = \
{'': ['*']}

extras_require = \
{'fastapi': ['fastapi>=0.72.0,<0.73.0'], 'redis': ['redis>=4.1.1,<5.0.0']}

setup_kwargs = {
    'name': 'throttled',
    'version': '0.1.0',
    'description': 'A rate limiter for FastAPI',
    'long_description': '',
    'author': 'Vinícius Vargas',
    'author_email': 'santunionivinicius@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/santunioni/ThrottledAPI',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
