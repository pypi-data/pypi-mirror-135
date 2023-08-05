# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['droughty_dev']

package_data = \
{'': ['*']}

install_requires = \
['GitPython==3.1.26',
 'PyYAML==6.0',
 'SQLAlchemy==1.4.22',
 'click==8.0.1',
 'lkml==1.1.0',
 'pandas-gbq==0.15.0',
 'pandas==1.3.1',
 'protobuf==3.19.3',
 'pycryptodomex==3.10.1',
 'ruamel.base==1.0.0',
 'ruamel.yaml>=0.17.20,<0.18.0',
 'snowflake-connector-python>=2.7.2,<3.0.0',
 'snowflake-sqlalchemy>=1.3.3,<2.0.0',
 'snowflake==0.0.3']

entry_points = \
{'console_scripts': ['droughty = droughty_cli:cli']}

setup_kwargs = {
    'name': 'droughty-dev',
    'version': '0.1.12',
    'description': '',
    'long_description': None,
    'author': 'Lewis',
    'author_email': 'lewischarlesbaker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
