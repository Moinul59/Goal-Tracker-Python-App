#!/bin/bash
set -e

echo "Waiting for postgres..."
while ! nc -z db 5432; do
    sleep 1
done

echo "Postgres is up"

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
