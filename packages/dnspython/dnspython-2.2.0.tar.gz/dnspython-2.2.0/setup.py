# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dns', 'dns.rdtypes', 'dns.rdtypes.ANY', 'dns.rdtypes.CH', 'dns.rdtypes.IN']

package_data = \
{'': ['*']}

extras_require = \
{'curio': ['curio>=1.2,<2.0', 'sniffio>=1.1,<2.0'],
 'dnssec': ['cryptography>=2.6,<37.0'],
 'doh': ['requests-toolbelt>=0.9.1,<0.10.0', 'requests>=2.23.0,<3.0.0'],
 'doh:python_full_version >= "3.6.2"': ['httpx>=0.21.1', 'h2>=4.1.0'],
 'idna': ['idna>=2.1,<4.0'],
 'trio': ['trio>=0.14,<0.20'],
 'wmi': ['wmi>=1.5.1,<2.0.0']}

setup_kwargs = {
    'name': 'dnspython',
    'version': '2.2.0',
    'description': 'DNS toolkit',
    'long_description': None,
    'author': 'Bob Halley',
    'author_email': 'halley@dnspython.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
