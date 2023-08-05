# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['erd_python']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'ply>=3.11', 'pygraphviz>=1.6']

setup_kwargs = {
    'name': 'erd-python',
    'version': '0.6.0',
    'description': 'Generate ERD diagrams using python',
    'long_description': None,
    'author': 'Datateer',
    'author_email': 'dev@datateer.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
