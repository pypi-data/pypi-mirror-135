# golos-lib-python

Официальная библиотека Golos для Python. Форк библиотеки [golodranets](https://github.com/steepshot/golodranets). Актуально на HF 26 и находится в активной разработке.

Включает в себя все необходимое для работы с GOLOS: формирование, подписывание и отправка транзакций, получение данных от API, работа с криптографией. Кроме того, присутствует BIP38-кошелек для шифрования приватных ключей.

Подходит для торговых ботов, скриптов, автоматических шлюзов, для SSR и микросервисов на Python. Может применяться в десктопных и мобильных приложениях (Kivy).

# Установка

Как обычный пакет:

```sh
pip install golos-lib-python
```

Или можно собрать из исходников:

```sh
cd golos-lib-python
poetry install
poetry build
```

Для запуска тестов:
```sh
poetry run pytest
```

## Сборка для macOS

Перед сборкой выполните:

```sh
brew install openssl
export CFLAGS="-I$(brew --prefix openssl)/include $CFLAGS"
export LDFLAGS="-L$(brew --prefix openssl)/lib $LDFLAGS"
```
