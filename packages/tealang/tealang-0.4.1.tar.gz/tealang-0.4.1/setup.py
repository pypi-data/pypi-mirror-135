# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tea',
 'tea.helpers',
 'tea.helpers.constants',
 'tea.logging',
 'tea.runtimeDataStructures',
 'tea.z3_solver']

package_data = \
{'': ['*']}

install_requires = \
['attrs==21.4.0',
 'bootstrapped==0.0.2',
 'pandas==1.3.5',
 'parameterized==0.8.1',
 'requests==2.27.1',
 'scikit-learn==1.0.2',
 'scipy==1.7.3',
 'statsmodels>=0.12.2,<0.13.0',
 'sympy==1.9',
 'urllib3==1.26.8',
 'z3-solver==4.8.14.0']

setup_kwargs = {
    'name': 'tealang',
    'version': '0.4.1',
    'description': 'Tea: A High-level Language and Runtime System to Automate Statistical Analysis',
    'long_description': None,
    'author': 'Eunice Jun',
    'author_email': 'eunice.m.jun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.11,<3.11',
}


setup(**setup_kwargs)
