# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datateer_cli', 'datateer_cli.docs', 'datateer_cli.pipeline']

package_data = \
{'': ['*'], 'datateer_cli': ['flow/*', 'ssh/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'boto3>=1.20.37,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'erd-python>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'datateer-cli',
    'version': '0.3.2',
    'description': 'Datateer CLI to support devops and infrastructure',
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
