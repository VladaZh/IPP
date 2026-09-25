#!/bin/sh

echo "Проверка и применение миграций базы данных..."
python -m alembic upgrade head

if [ $? -ne 0 ]; then
    echo "Ошибка при применении миграций!"
    exit 1
fi

echo "Миграции применены. Запуск приложения..."
exec "$@"