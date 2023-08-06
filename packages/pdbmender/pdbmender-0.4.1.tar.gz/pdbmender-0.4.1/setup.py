# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdbmender',
 'pdbmender.pdb2pqr',
 'pdbmender.pdb2pqr.conf_avg',
 'pdbmender.pdb2pqr.extensions',
 'pdbmender.pdb2pqr.src']

package_data = \
{'': ['*'], 'pdbmender.pdb2pqr': ['dat/*', 'tools/*']}

setup_kwargs = {
    'name': 'pdbmender',
    'version': '0.4.1',
    'description': 'Mend PDB files',
    'long_description': None,
    'author': 'Pedro B.P.S. Reis',
    'author_email': 'pdreis@fc.ul.pt',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
