# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybgpranking2']

package_data = \
{'': ['*']}

install_requires = \
['pyipasnhistory>=2.1,<3.0', 'requests>=2.26.0,<3.0.0']

extras_require = \
{'docs': ['Sphinx>=4.3,<5.0']}

entry_points = \
{'console_scripts': ['bgpranking = pybgpranking2:main']}

setup_kwargs = {
    'name': 'pybgpranking2',
    'version': '2.0.1',
    'description': 'Python CLI and module for BGP Ranking',
    'long_description': '# Python client and module for BGP Ranking\n\nTHis project will make querying BGP Ranking easier.\n\n## Installation\n\n```bash\npip install pybgpranking\n```\n\n## Usage\n\n### Command line\n\nYou can use the `bgpranking` command to query the instance:\n\n```bash\n```\n\n### Library\n\nSee [API Reference]()\n',
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
