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
    'version': '0.0.5',
    'description': 'rabbitmq-subprocess-client is a RabbitMQ client (based on `pika`) spawning tasks as subprocess, allowing handling segfault gracefully.',
    'long_description': 'RabbitMQ-subprocess-client\n=====================\n\nRabbitMQ-subprocess-client is a RabbitMq client (based on `pika`) spawning tasks as subprocess, allowing handling segfault gracefully. \n\n\n# Install\n```bash\npip install rabbitmq-subprocess-client\n```\n\n# usage\n```python\nimport os\nfrom concurrent.futures import TimeoutError\nimport traceback\nfrom rabbitmq_subprocess_client import Runner, Consumer\n\nclass MyConsumer(Consumer):\n    def consume_main(self, basic_deliver, msg):\n        print(f\'pre-processing message: {msg} in process: {os.getpid()}\')\n        try:\n            args = []\n            kwargs = {}\n            self.exec(msg, *args, **kwargs)  # This will run the consume_subprocess method in a subprocess\n            self.acknowledge_message(basic_deliver.delivery_tag)\n        except TimeoutError:\n            self.nacknowledge_message(basic_deliver.delivery_tag)\n        except BaseException:\n            exc_msg = traceback.format_exc()\n            print(exc_msg)\n            self.nacknowledge_message(basic_deliver.delivery_tag)\n\n    @staticmethod\n    def consume_subprocess(msg, *args, **kwargs):\n        print(f\'processing message: {msg} in process: {os.getpid()}\')\n\nworker = Runner(\n    \'my_queue\', \n    MyConsumer, \n    host="127.0.0.1",\n    port="5672",\n    user="guest",\n    password="guest",\n    timeout=None,\n)\nworker.run()\n```\n\n    \n# develop\n```bash\npoetry shell\npoetry install\npytest\npre-commit install\n```\n\n# Publish new version\n```bash\npoetry publish --build --username= --password=\n```\n',
    'author': 'amoki',
    'author_email': 'hugo@bimdata.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bimdata/rabbitmq-subprocess-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
