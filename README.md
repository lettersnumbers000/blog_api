# Blog API

Запуск: `docker compose up --build`, документация: http://localhost:8001/docs

Тесты: `pip install -r requirements.txt && pytest`

Первый зарегистрированный пользователь получает роль admin (может удалять посты и смотреть список пользователей).

Деплой на Railway: создать проект из GitHub-репозитория, добавить плагины PostgreSQL и Redis, задать переменные DATABASE_URL, REDIS_URL, SECRET_KEY, CORS_ORIGIN. Для воркера создать второй сервис из того же репозитория со стартовой командой `celery -A app.celery_app worker --loglevel=info`.
