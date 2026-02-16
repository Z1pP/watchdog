# Watchdog

Сервис для отслеживания цен товаров в маркетплейсах (Ozon, Wildberries): подписки на товары и уведомления при снижении цены.

## Стек

- Python 3.13+, Django 6.x
- PostgreSQL (psycopg)
- Управление зависимостями: **uv**
- Переменные окружения: **python-dotenv**, конфиг в `.env`

## Установка и запуск

1. Клонируйте репозиторий и перейдите в каталог проекта.

2. Установите зависимости:
   ```bash
   uv sync
   ```

3. Создайте файл `.env` в корне проекта (см. раздел «Переменные окружения»). Файл `.env` не коммитится в репозиторий.

4. Примените миграции:
   ```bash
   uv run python watchdog/manage.py migrate
   ```

5. Запустите сервер:
   ```bash
   uv run python watchdog/manage.py runserver
   ```
   Или из каталога `watchdog`:
   ```bash
   cd watchdog && uv run python manage.py runserver
   ```

6. Создайте суперпользователя для входа в админку:
   ```bash
   uv run python watchdog/manage.py createsuperuser
   ```

Админка: http://127.0.0.1:8000/admin/

## Структура проекта

- **watchdog/** — корень Django-проекта (`manage.py`, приложения)
- **watchdog/account** — пользователи и провайдеры входа (email, Google, Telegram)
- **watchdog/product** — маркетплейсы, товары, офферы, история цен, подписки на товары
- **watchdog/watchdog** — настройки, URL, WSGI/ASGI

## Переменные окружения (.env)

| Переменная | Описание |
|------------|----------|
| `SECRET_KEY` | Секретный ключ Django (обязательно) |
| `DEBUG` | `True` / `False` (по умолчанию для разработки — True) |
| `DB_USER` | Пользователь PostgreSQL |
| `DB_HOST` | Хост PostgreSQL |
| `DB_PORT` | Порт PostgreSQL (например 5432) |
| `DB_NAME` | Имя базы данных |
| `DB_PASSWORD` | Пароль PostgreSQL |
| `PRICE_UPDATE_INTERVAL_MINUTES` | Интервал обновления цен в минутах (опционально, по умолчанию 30) |

Файл `.env` не коммитится в репозиторий (указан в `.gitignore`).
