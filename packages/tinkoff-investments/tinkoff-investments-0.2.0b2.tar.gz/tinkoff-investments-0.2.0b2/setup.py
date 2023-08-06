# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinkoff', 'tinkoff.invest', 'tinkoff.invest.grpc']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.39.0,<2.0.0', 'protobuf>=3.19.3,<4.0.0', 'tinkoff>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'tinkoff-investments',
    'version': '0.2.0b2',
    'description': '',
    'long_description': None,
    'author': 'Danil Akhtarov',
    'author_email': 'd.akhtarov@tinkoff.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
