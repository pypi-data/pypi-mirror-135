# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hipopy']

package_data = \
{'': ['*']}

install_requires = \
['awkward>=1.7.0,<2.0.0', 'numpy>=1.22.1,<2.0.0']

setup_kwargs = {
    'name': 'hipopy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Matthew McEneaney',
    'author_email': 'matthew.mceneaney@duke.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
