# TradeUnion_Bot

## Серверная часть

### Инструкция по поднятию сервера:

Запонить файл с перемнными огружения *".env"*.
Находясь в дериктории *"server"* выполнить команду:

```sh
docker-compose up
```

Тесты запускаются по команде:

```sh
docker-compose -f docker-compose-test.yaml up
```

## Бот

### Инструкция по поднятию бота:

После запуска сервера, находясь в дериктории *"bot"* выполнить команду:

```sh
docker-compose up
```

### Стек технологий:

* FastAPI
* Uvicorn
* MongoDB
* Aiogram
* Redis
* Pytest
* Docker

