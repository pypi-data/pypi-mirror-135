# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rabbitmq_subprocess_client']

package_data = \
{'': ['*']}

install_requires = \
['pika>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'rabbitmq-subprocess-client',
    'version': '0.0.4',
    'description': 'RabbitMQ client spawning tasks in a subprocess',
    'long_description': None,
    'author': 'amoki',
    'author_email': 'hugo@bimdata.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
