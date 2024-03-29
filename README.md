# Дипломный проект Yandex.Praktikum: Foodgram

## Цель проекта
Проверить и закрепить полученные знания по разработке веб-приложений на Django.

## Описание
Сервис для публикации рецептов. Пользователи могут публиковать свои рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в избранное и создавать список покупок.

## Технологии
- Python 3.10
- Django 3.2
- PostgreSQL 13
- Docker
- Nginx
- Gunicorn

## Запуск проекта
1. Склонировать репозиторий
2. В папке infra создать файл .env и заполнить его переменными окружения (пример в .env.example)
3. В папке infra выполнить команду `docker-compose up -d`
4. Перейти по адресу `http://localhost/`
5. Для создания суперпользователя выполнить команду `docker exec backend python manage.py createsuperuser`
6. Документация API доступна по адресу `http://localhost/api/docs/`

## Дополнительные варианты реализации передачи контекста через annotate и через менеджер контекста (ради интереса) можно посмотреть в ветках context_annotate и manager_models