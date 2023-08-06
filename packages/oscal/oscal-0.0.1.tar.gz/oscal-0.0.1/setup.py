# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oscal']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'oscal',
    'version': '0.0.1',
    'description': '',
    'long_description': '# PyOSCAL',
    'author': 'Guy Zylberberg',
    'author_email': 'guyzyl@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
