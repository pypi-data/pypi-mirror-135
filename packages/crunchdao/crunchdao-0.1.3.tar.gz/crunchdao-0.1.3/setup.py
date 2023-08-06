# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crunchdao']

package_data = \
{'': ['*']}

install_requires = \
['inflection>=0.5.1,<0.6.0',
 'pandas>=1.3.5,<2.0.0',
 'requests>=2.27.0,<3.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'crunchdao',
    'version': '0.1.3',
    'description': 'Python API for the Crunchdao machine learning tournament',
    'long_description': None,
    'author': 'uuazed',
    'author_email': 'uuazed@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
