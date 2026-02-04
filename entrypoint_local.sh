#!/bin/bash
set -e

# If the first argument looks like the app server, do setup
if [ "$1" = "gunicorn" ] || [ "$1" = "flask" ]; then
    echo "Starting application..."

    if [ -n "$DATABASE_HOST" ]; then
        echo "Waiting for postgres at $DATABASE_HOST:${DATABASE_PORT:-5432}..."
        while ! nc -z "$DATABASE_HOST" "${DATABASE_PORT:-5432}"; do
            sleep 1
        done
        echo "Postgres is up"
    fi
fi

# ✅ Run migrations only once
if [ ! -f "/app/.migrated" ]; then
    echo "Running migrations for the first time..."
    flask db upgrade
    touch /app/.migrated
else
    echo "Migrations already applied, skipping..."
fi

echo "Starting application..."
exec "$@"
