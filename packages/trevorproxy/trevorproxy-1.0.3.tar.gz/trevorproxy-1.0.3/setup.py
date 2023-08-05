# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trevorproxy', 'trevorproxy.lib']

package_data = \
{'': ['*']}

install_requires = \
['sh>=1.14.2,<2.0.0']

entry_points = \
{'console_scripts': ['trevorproxy = trevorproxy.cli:main']}

setup_kwargs = {
    'name': 'trevorproxy',
    'version': '1.0.3',
    'description': 'Rotate your source IP address via SSH proxies and other methods',
    'long_description': None,
    'author': 'TheTechromancer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
