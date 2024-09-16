# Tender Service

## Описание проекта

Этот проект представляет собой сервис для управления тендерами и ставками. Он разработан на Django и использует Django REST Framework для создания API. 

## Функциональные возможности

- Управление тендерами
- Управление ставками
- Пинг эндпоинт для проверки доступности сервиса

## Установка и запуск

### Клонирование репозитория

```
git clone https://github.com/Ydtalel/tender_api.git
```
`cd tender_api`

Необходима версия python **3.12** или новее.

python -m venv .venv  
source .venv/bin/activate # На Windows используйте .venv\Scripts\activate

### Установка зависимостей

`pip install -r requirements.txt`

### Переменные окружения

Создайте файл .env в корневой директории приложения

Задайте параметры вашей базы данных

POSTGRES_DATABASE=<your_database_name>  
POSTGRES_USERNAME=<your_username>  
POSTGRES_PASSWORD=<your_password>   
POSTGRES_HOST=<your_host>  
POSTGRES_PORT=<your_port>   

### Настройка базы данных
`python manage.py makemigrations`

`python manage.py migrate`
### Запуск сервера
`python manage.py runserver`

Приложение будет доступно по адресу: http://localhost:8000/api/tenders.

### Swagger UI
Документация вашего API доступна через Swagger UI по адресу: http://localhost:8000/swagger/
