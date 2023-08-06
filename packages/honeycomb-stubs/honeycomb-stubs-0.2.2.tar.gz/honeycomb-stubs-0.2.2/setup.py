# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beeline-stubs', 'libhoney-stubs']

package_data = \
{'': ['*'], 'beeline-stubs': ['propagation/*']}

install_requires = \
['honeycomb-beeline>=3.0.0,<4.0.0', 'libhoney>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'honeycomb-stubs',
    'version': '0.2.2',
    'description': 'Type stubs for the libhoney and beeline packages',
    'long_description': '# honeycomb-stubs\n\n[![PyPI](https://img.shields.io/pypi/v/honeycomb-stubs)](https://pypi.org/project/honeycomb-stubs/)\n\nPython type stubs for:\n\n  * [libhoney](https://github.com/honeycombio/libhoney-py)\n  * [beeline](https://github.com/honeycombio/beeline-python)\n\nThe stubs for `beeline` are relatively complete, but the stubs for `libhoney`\nare woefully incomplete. PRs welcome!\n\n## Usage\n\n```\npip install honeycomb-stubs\n```\n',
    'author': 'Nikhil Benesch',
    'author_email': 'nikhil.benesch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benesch/honeycomb-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
