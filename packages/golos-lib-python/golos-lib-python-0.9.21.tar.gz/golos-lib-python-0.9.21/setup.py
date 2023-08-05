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
    'version': '0.9.21',
    'description': 'Python library for Golos blockchain',
    'long_description': '# golos-lib-python\n\nОфициальная библиотека Golos для Python. Форк библиотеки [golodranets](https://github.com/steepshot/golodranets). Актуально на HF 26 и находится в активной разработке.\n\nВключает в себя все необходимое для работы с GOLOS: формирование, подписывание и отправка транзакций, получение данных от API, работа с криптографией. Кроме того, присутствует BIP38-кошелек для шифрования приватных ключей.\n\nПодходит для торговых ботов, скриптов, автоматических шлюзов, для SSR и микросервисов на Python. Может применяться в десктопных и мобильных приложениях (Kivy).\n\n# Установка\n\nКак обычный пакет:\n\n```sh\npip install golos-lib-python\n```\n\nИли можно собрать из исходников:\n\n```sh\ncd golos-lib-python\npoetry install\npoetry build\n```\n\nДля запуска тестов:\n```sh\npoetry run pytest\n```\n\n## Сборка для macOS\n\nПеред сборкой выполните:\n\n```sh\nbrew install openssl\nexport CFLAGS="-I$(brew --prefix openssl)/include $CFLAGS"\nexport LDFLAGS="-L$(brew --prefix openssl)/lib $LDFLAGS"\n```\n',
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
