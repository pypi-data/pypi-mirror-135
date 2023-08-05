# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['palette_generator']

package_data = \
{'': ['*']}

install_requires = \
['Wand', 'matplotlib', 'numpy', 'pandas', 'scipy>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'palette-generator',
    'version': '0.1.1',
    'description': '`palette_generator` is here to turn your images into beautiful palettes',
    'long_description': '\nInstallation\n============\n\n`pip install palette_generator`\n\nBasic Usage\n===========\n\n`python -m palette_generator -h`\n\nDocumentation\n=============\n\n[Find full documentation here!](https://neonfuzz.github.io/palette_generator/html/index.html)\n',
    'author': 'neonfuzz',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/neonfuzz/palette_generator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
