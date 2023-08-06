# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ak_vendor',
 'ak_vendor.compliances',
 'ak_vendor.migrations',
 'ak_vendor.report']

package_data = \
{'': ['*'],
 'ak_vendor': ['locale/ja/LC_MESSAGES/*', 'templates/*', 'translations/ja/*']}

install_requires = \
['attrs>=21.1.0',
 'black>=21.9b0,<22.0',
 'cvss>=2.0',
 'html2text==2020.1.16',
 'maya>=0.6.0',
 'orm-choices==0.3.0']

setup_kwargs = {
    'name': 'ak-vendor',
    'version': '4.0.2',
    'description': 'Some vendor scripts that we use here at Appknox',
    'long_description': None,
    'author': 'Appknox',
    'author_email': 'engineering@appknox.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/appknox/vendor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
