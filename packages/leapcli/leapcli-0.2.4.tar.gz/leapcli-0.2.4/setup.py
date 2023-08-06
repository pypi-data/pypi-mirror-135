# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leapcli']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.18,<4.0.0',
 'code-loader==0.1.15',
 'docopt>=0.6.2,<0.7.0',
 'luddite>=1.0.2,<2.0.0',
 'pytest-mock>=3.6.1,<4.0.0',
 'python-json-logger>=2.0.2,<3.0.0',
 'requests>=2.26.0,<3.0.0',
 'semver>=2.13.0,<3.0.0',
 'tensorleap-openapi-client==1.1.6',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['leap = cli:__main__']}

setup_kwargs = {
    'name': 'leapcli',
    'version': '0.2.4',
    'description': 'Tensorleap CLI',
    'long_description': None,
    'author': 'Assaf Lavie',
    'author_email': 'assaf.lavie@tensorleap.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tensorleap/cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<3.7',
}


setup(**setup_kwargs)
