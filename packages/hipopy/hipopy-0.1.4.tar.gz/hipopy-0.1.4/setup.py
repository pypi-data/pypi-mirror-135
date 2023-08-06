# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hipopy']

package_data = \
{'': ['*']}

install_requires = \
['awkward>=1.3.0,<2.0.0', 'numpy>=1.19.2,<2.0.0']

setup_kwargs = {
    'name': 'hipopy',
    'version': '0.1.4',
    'description': 'UpROOT-Like I/O Interface for CLAS12 HIPO Files',
    'long_description': None,
    'author': 'Matthew McEneaney',
    'author_email': 'matthew.mceneaney@duke.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mfmceneaney/hipopy.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
