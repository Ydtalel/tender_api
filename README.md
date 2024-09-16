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

python -m venv .venv  
source .venv/bin/activate # На Windows используйте .venv\Scripts\activate

### Установка зависимостей

`pip install -r requirements.txt`

### Настройка базы данных
`python manage.py makemigrations`

`python manage.py migrate`
### Запуск сервера
`python manage.py runserver`

Приложение будет доступно по адресу: http://localhost:8000.

### Swagger UI
Документация вашего API доступна через Swagger UI по адресу: http://localhost:8000/swagger/
