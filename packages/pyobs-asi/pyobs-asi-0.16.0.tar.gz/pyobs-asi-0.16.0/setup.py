# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyobs_asi']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=5.0,<6.0',
 'numpy>=1.21,<2.0',
 'pyobs-core>=0.16.1,<0.17.0',
 'zwoasi>=0.1,<0.2']

setup_kwargs = {
    'name': 'pyobs-asi',
    'version': '0.16.0',
    'description': 'pyobs model for ASI cameras',
    'long_description': None,
    'author': 'Tim-Oliver Husser',
    'author_email': 'thusser@uni-goettingen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
