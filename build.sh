#!/usr/bin/env bash
# Скрипт збірки для Render
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
# Страховка: якщо файл міграції не потрапив у репозиторій, створити його
python manage.py makemigrations restaurant --no-input
python manage.py migrate --no-input

# Створити адміна автоматично (якщо задані змінні), без помилки якщо вже існує
if [[ -n "${DJANGO_SUPERUSER_USERNAME:-}" && -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]]; then
  python manage.py createsuperuser --no-input --email "${DJANGO_SUPERUSER_EMAIL:-admin@example.com}" || true
fi

# Прикладові страви (скрипт не дублює записи)
if [[ "${SEED_DATA:-false}" == "true" ]]; then
  python seed_data.py
fi
