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
    'version': '0.4.2',
    'description': 'Tea: A High-level Language and Runtime System to Automate Statistical Analysis',
    'long_description': '# tea-lang [![Build Status](https://travis-ci.com/tea-lang-org/tea-lang.svg?branch=master)](https://travis-ci.com/tea-lang-org/tea-lang) [![Coverage Status](https://coveralls.io/repos/github/tea-lang-org/tea-lang/badge.svg?branch=master)](https://coveralls.io/github/tea-lang-org/tea-lang?branch=master)\n\n# [WIP] Tea: A High-level Language and Runtime System for Automating Statistical Analyses\n\n## What is Tea?\nTea is a domain specific programming language that automates statistical test\nselection and execution. Tea is currently written in/for Python. \n\nTea has an <a href=\'http://tea-lang.org/index_files/tea_UIST2019.pdf\'>academic research paper</a>. \n\nUsers provide 5 pieces of information: \n* the *dataset* of interest, \n* the *variables* in the dataset they want to analyze, \n* the *study design* (e.g., independent, dependent variables),\n* the *assumptions* they make about the data based on domain knowledge(e.g.,\na variable is normally distributed), and\n* a *hypothesis*.\n\nTea then "compiles" these into logical constraints to select valid\nstatistical tests. Tests are considered valid if and only if *all* the\nassumptions they make about the data (e.g., normal distribution, equal\nvariance between groups, etc.) hold. Tea then finally executes the valid tests.\n\n## What kinds of statistical analyses are possible with Tea?\nTea currently provides a module to conduct Null Hypothesis Significance\nTesting (NHST). \n\n*We are actively working on expanding the kinds of analyses Tea can support. Some ideas we have: linear modeling and Bayesian inference.*\n\n## How can I use Tea?\n<a href=\'https://pypi.org/project/tealang/\'>Tea is available on pip!</a>\n```\npip install tealang\n```\n\nSee community examples <a href=\'https://github.com/tea-lang-org/tea-lang/tree/master/examples\'>here</a>. If you have trouble using Tea with your use case, feel free to open an issue, and we\'ll try to help. \n\nStep through <a href=\'https://github.com/tea-lang-org/tea-lang/blob/master/documentation.md\'>a more guided, thorough documentation and a worked example</a>. \n\n## How can I cite Tea?\nFor now, please cite: \n```  \narticle{JunEtAl2019:Tea,\n  title={Tea: A High-level Language and Runtime System for Automating Statistical Analysis},\n  author={Jun, Eunice and Daum, Maureen and Roesch, Jared and Chasins, Sarah E. and Berger, Emery D. and Just, Rene and Reinecke, Katharina},\n  journal={Proceedings of the 32nd Annual ACM Symposium on User Interface Software and Technology (UIST)},\n  year={2019}\n}\n```\n\n## How reliable is Tea?\nTea is currently a research prototype. Our constraint solver is based on\nstatistical texts (see <a href=\'http://tea-lang.org/index_files/tea_UIST2019.pdf\'>our paper</a> for more info). \n\nIf you find any bugs, please let us know (email Eunice at emjun [at] cs.washington.edu)!\n\n## I want to collaborate! Where do I begin?\nThis is great! We\'re excited to have new collaborators. :) \n\nTo contribute *code*, please see <a href=\'./CONTRIBUTING.md\'> docs and\ngudielines</a> and open an issue or pull request. \n\nIf you want to use Tea for a\nproject, talk about Tea\'s design, or anything else, please get in touch: emjun [at] cs.washington.edu!\n\n## Where can I learn more about Tea?\nPlease find more information at <a href=\'https://tea-lang.org\'>our website</a>. \n\n## I have ideas. I want to chat. \nPlease reach out! We are nice :) Email Eunice at emjun [at] cs.washington.edu!\n\n\n## FAQs\n### By the way, why Python?\nPython is a common language for data science. We hope Tea can easily integrate\ninto user workflows. \n\n### What format should my data be in?\nTea accepts data either as a CSV or a Pandas DataFrame. Tea asumes data is in <a href=\'http://www.cookbook-r.com/Manipulating_data/Converting_data_between_wide_and_long_format/\'>"long format."</a> \n',
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
