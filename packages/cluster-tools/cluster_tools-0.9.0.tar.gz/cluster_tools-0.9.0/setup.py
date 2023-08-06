# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cluster_tools', 'cluster_tools.schedulers']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'cluster-tools',
    'version': '0.9.0',
    'description': 'Utility library for easily distributing code execution on clusters',
    'long_description': None,
    'author': 'scalable minds',
    'author_email': 'hello@scalableminds.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
