# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cherryadmin']

package_data = \
{'': ['*']}

install_requires = \
['nxtools>=1.6,<2.0']

entry_points = \
{'console_scripts': ['docs = scripts:docs', 'test = scripts:test']}

setup_kwargs = {
    'name': 'cherryadmin',
    'version': '5.21',
    'description': 'CherryPy admin framework',
    'long_description': 'CherryAdmin\n===========\n',
    'author': 'Martin Wacker',
    'author_email': 'martas@imm.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/martastain/cherryadmin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
