# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kalong', 'kalong.utils', 'kalong.utils.doc_lookup']

package_data = \
{'': ['*'], 'kalong': ['static/*', 'static/assets/*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'jedi>=0.18.1,<0.19.0']

setup_kwargs = {
    'name': 'kalong',
    'version': '0.2.1',
    'description': 'A new take on python debugging',
    'long_description': None,
    'author': 'Florian Mounier',
    'author_email': 'paradoxxx.zero@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/paradoxxxzero/kalong',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
