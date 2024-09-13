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
git clone https://git.codenrock.com/avito-testirovanie-na-backend-1270/cnrprod1725864137-team-77037/tender_service.git
cd tender_service
```
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
