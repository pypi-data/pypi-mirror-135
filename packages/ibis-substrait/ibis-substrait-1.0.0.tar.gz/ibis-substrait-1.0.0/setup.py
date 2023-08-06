# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ibis_substrait',
 'ibis_substrait.compiler',
 'ibis_substrait.proto',
 'ibis_substrait.proto.substrait',
 'ibis_substrait.proto.substrait.extensions',
 'ibis_substrait.tests',
 'ibis_substrait.tests.compiler']

package_data = \
{'': ['*']}

install_requires = \
['ibis-framework>=2.0.0,<3.0.0', 'inflection>=0.5.1,<0.6.0']

setup_kwargs = {
    'name': 'ibis-substrait',
    'version': '1.0.0',
    'description': 'Subtrait compiler for ibis',
    'long_description': "# [Ibis](https://ibis-project.org) + [Substrait](https://substrait.io)\n\nThis repo houses the Substrait compiler for ibis.\n\nWe're just getting started here, so stay tuned!\n",
    'author': 'Ibis Contributors',
    'author_email': None,
    'maintainer': 'Ibis Contributors',
    'maintainer_email': None,
    'url': 'https://github.com/ibis-project/ibis-substrait',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
