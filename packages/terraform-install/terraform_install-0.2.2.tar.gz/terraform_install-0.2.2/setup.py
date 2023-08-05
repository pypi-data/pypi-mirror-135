# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terraform_install', 'terraform_install.cli']

package_data = \
{'': ['*']}

install_requires = \
['terraform_version']

entry_points = \
{'console_scripts': ['terraform = terraform_install.terraform:terraform']}

setup_kwargs = {
    'name': 'terraform-install',
    'version': '0.2.2',
    'description': 'Wrapper which installs Terraform',
    'long_description': None,
    'author': 'Josh Wycuff',
    'author_email': 'Joshua.Wycuff@turner.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joshwycuff/python-terraform-utils/packages/terraform_install',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
