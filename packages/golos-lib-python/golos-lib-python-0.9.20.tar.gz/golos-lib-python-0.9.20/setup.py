# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['golos', 'golosbase']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'certifi>=2020.4.5,<2021.0.0',
 'ecdsa>=0.13,<0.14',
 'funcy>=1.14,<2.0',
 'langdetect>=1.0.8,<2.0.0',
 'prettytable>=0.7.2,<0.8.0',
 'pycryptodome>=3.9.7,<4.0.0',
 'pylibscrypt>=1.8.0,<2.0.0',
 'scrypt>=0.8.13,<0.9.0',
 'toolz>=0.10.0,<0.11.0',
 'ujson>=2.0.3,<3.0.0',
 'urllib3>=1.25.9,<2.0.0',
 'voluptuous>=0.11.7,<0.12.0',
 'w3lib>=1.21.0,<2.0.0',
 'websocket-client>=0.56,<0.57']

setup_kwargs = {
    'name': 'golos-lib-python',
    'version': '0.9.20',
    'description': 'Python library for Golos blockchain',
    'long_description': '# Python GOLOS Library\n\nThis is a fork of [golodranets](https://github.com/steepshot/golodranets) GOLOS\nlibrary for Python which was forked from official STEEM library for Python. It\ncomes with a BIP38 encrypted wallet.\n\nThe main differences from the `steem-python`:\n\n* directed to work with GOLOS blockchain\n* websocket support\n* convert Cyrillic to Latin for tags and categories\n* Golos assets - `STEEM` -> `GOLOS`, `SBD` -> `GBG`, `VESTS` -> `GESTS`\n* renamed modules - `steem` -> `golos`, `steemdata` -> `golosdata`\n* for `Post` instance added two fields - `score_trending` and `score_hot`. This fields may be helpful if you want to sort your saved posts like `get_discussions_by_trending` and `get_discussions_by_trending` methods do. `reblogged_by` field is also filled now\n* for `Account` instance methods `get_followers` and `get_following` were improved - now it takes `limit` and `offset` parameters\n\nGOLOS HF 26 is supported.\n\n# Installation\n\nAs regular package:\n\n```\npip install python-golos\n```\n\nLocal installation from source:\n\n```\ncd golos-python\npoetry install\npoetry shell\n```\n\n## Homebrew Build Prereqs\n\nIf you\'re on a mac, you may need to do the following first:\n\n```\nbrew install openssl\nexport CFLAGS="-I$(brew --prefix openssl)/include $CFLAGS"\nexport LDFLAGS="-L$(brew --prefix openssl)/lib $LDFLAGS"\n```\n',
    'author': 'Vladimir Kamarzin',
    'author_email': 'vvk@vvk.pp.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/golos-blockchain/lib-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
