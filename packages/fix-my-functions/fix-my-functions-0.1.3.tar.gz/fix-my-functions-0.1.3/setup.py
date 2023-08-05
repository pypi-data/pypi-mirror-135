# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fix_my_functions']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4', 'redbaron>=0.9.2']

entry_points = \
{'console_scripts': ['fix-my-functions = fix_my_functions.__main__:main']}

setup_kwargs = {
    'name': 'fix-my-functions',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Peder Bergebakken Sundt',
    'author_email': 'pbsds@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
