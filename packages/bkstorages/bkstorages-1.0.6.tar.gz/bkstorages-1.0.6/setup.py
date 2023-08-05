# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bkstorages', 'bkstorages.backends']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.4.1', 'curlify>=2.2.1,<3.0.0', 'requests', 'six']

setup_kwargs = {
    'name': 'bkstorages',
    'version': '1.0.6',
    'description': 'File storage backends for blueking PaaS platform',
    'long_description': None,
    'author': 'blueking',
    'author_email': 'blueking@tencent.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<3.8',
}


setup(**setup_kwargs)
