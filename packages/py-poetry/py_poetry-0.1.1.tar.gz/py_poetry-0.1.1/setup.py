# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_poetry']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'py-poetry',
    'version': '0.1.1',
    'description': 'LOL',
    'long_description': None,
    'author': 'Qaminono',
    'author_email': '36382154+Qaminono@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
