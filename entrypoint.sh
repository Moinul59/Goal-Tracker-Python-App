#!/bin/bash
set -e

echo "Container starting..."

# Wait for Postgres ONLY if app server is starting
if [ "$1" = "gunicorn" ] || [ "$1" = "flask" ]; then
    if [ -n "$DATABASE_HOST" ]; then
        echo "Waiting for Postgres at ${DATABASE_HOST}:${DATABASE_PORT:-5432}..."

        until nc -z "$DATABASE_HOST" "${DATABASE_PORT:-5432}"; do
            sleep 1
        done

        echo "Postgres is reachable"
    fi
fi

echo "Starting application..."
exec "$@"
