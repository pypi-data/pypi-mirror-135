# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orionapi']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0', 'tabulate>=0.8.9,<0.9.0']

setup_kwargs = {
    'name': 'orionapi',
    'version': '0.1.4',
    'description': 'A python interface for the Orion Advisors platform web API',
    'long_description': None,
    'author': 'spencerogden-dsam',
    'author_email': '67068943+spencerogden-dsam@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
