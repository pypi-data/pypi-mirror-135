# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ligo', 'ligo.em_bright', 'ligo.em_bright.tests']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.0',
 'h5py>=2.10.0',
 'htcondor>=9.0.6',
 'lalsuite>=7.0,<8.0',
 'pandas>=1.0,<2.0',
 'scikit-learn>=0.24,<0.25']

entry_points = \
{'console_scripts': ['em_bright_categorize = ligo.em_bright.categorize:main',
                     'em_bright_dag_writer = ligo.em_bright.dag_writer:main',
                     'em_bright_extract = ligo.em_bright.utils:extract',
                     'em_bright_join = ligo.em_bright.utils:join',
                     'em_bright_train = ligo.em_bright.utils:train']}

setup_kwargs = {
    'name': 'ligo.em-bright',
    'version': '0.1.5',
    'description': 'Possibility and properties of Electromagnetically-bright sources of gravitational-wave events',
    'long_description': None,
    'author': 'Deep Chatterjee',
    'author_email': 'deep.chatterjee@ligo.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
