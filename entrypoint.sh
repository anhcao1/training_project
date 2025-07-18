#!/bin/sh

set -e  # Exit immediately on error

echo "Waiting for PostgreSQL to become available at $DB_HOST:$DB_PORT..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done

echo "PostgreSQL is available - running migrations"
python manage.py migrate

echo "Starting service: $@"
exec "$@"