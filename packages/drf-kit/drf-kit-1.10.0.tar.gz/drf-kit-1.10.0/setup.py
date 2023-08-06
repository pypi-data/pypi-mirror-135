# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drf_kit', 'drf_kit.models', 'drf_kit.views']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3,<4',
 'django-filter>=2,<3',
 'django-ordered-model>=3,<4',
 'djangorestframework>=3,<4',
 'drf-extensions>=0,<1']

setup_kwargs = {
    'name': 'drf-kit',
    'version': '1.10.0',
    'description': 'DRF Toolkit',
    'long_description': None,
    'author': 'eduK',
    'author_email': 'pd@eduk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
