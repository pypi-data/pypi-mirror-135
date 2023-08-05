# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['iplocbuild']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'junos-eznc>=2.6.2,<3.0.0',
 'lxml>=4.6.5,<5.0.0',
 'netaddr>=0.8.0,<0.9.0']

entry_points = \
{'console_scripts': ['iplocbuild = iplocbuild.cli:cli']}

setup_kwargs = {
    'name': 'iplocbuild',
    'version': '1.0.4',
    'description': 'Command line too to generate IP Location files from routes found on network devices.',
    'long_description': '# iplocbuild\n\nBuild IP Location files from routes on network devices\n\n',
    'author': 'Rob Woodward',
    'author_email': 'rob@emailplus.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/robwdwd/iplocbuild',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
