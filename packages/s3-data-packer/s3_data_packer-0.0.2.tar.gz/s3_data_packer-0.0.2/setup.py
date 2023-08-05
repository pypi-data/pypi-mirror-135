# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3_data_packer']

package_data = \
{'': ['*']}

install_requires = \
['arrow-pd-parser>=1.0.3,<2.0.0',
 'awswrangler>=2.11.0,<3.0.0',
 'dataengineeringutils3>=1.2.1,<2.0.0',
 'mojap-metadata>=1.3,<2.0',
 'numpy>=1.21.2,<2.0.0']

setup_kwargs = {
    'name': 's3-data-packer',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 's-ducks',
    'author_email': 'stephen.bias@digital.justice.gov.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
