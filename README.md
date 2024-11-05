# Название проекта

## Описание проекта

Этот проект представляет собой тестовое задание от компании RePlace.

## Установка и запуск

### Предварительные требования

- Python 3.10+
- Poetry
- Make

### Установка

1. Клонируйте репозиторий:
   ```sh
   git clone https://github.com/AndyRetroWave/Test_Movies.git
   ```
2. Перейдите в директорию проекта:
   ```sh
   cd SocialBlog_User
   ```
3. Установите зависимости:
   ```sh
   poetry install
   ```
4. Поменяйте наименования для .env-copy на .env

5. Вставте в .env API_KEY_KINOPOISK свой токен API от кинопоиска.

6. Создайте базу данных Postgresql пароли и наименования должны совподать с файлом .env

7. Cделайте миграции через Alembic
   ```sh
   alembic upgrade head
   ```

### Запуск

1. Запустите сервер разработки:
   ```sh
   uvicorn main:app --reload
   ```
2. Откройте браузер и перейдите по адресу:
   ```
   http://localhost:8000/docs
   ```

### Запуск через Docker

1. Через docker-compose
   ```sh
   docker-compose up --build
   ```

### Тестирование

1. Запустите тесты:
   ```sh
   pytest
   ```
