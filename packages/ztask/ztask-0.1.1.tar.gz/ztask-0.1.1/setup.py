# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['ztask']
install_requires = \
['pandas>=1.3.5,<2.0.0', 'parsedatetime>=2.6,<3.0', 'prettyprint>=0.1.5,<0.2.0']

entry_points = \
{'console_scripts': ['ztask = ztask:main']}

setup_kwargs = {
    'name': 'ztask',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Pablo Ruiz',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
