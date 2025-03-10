#!/bin/bash

# Wait for database to be ready
if [ "$POSTGRES_HOST" = "postgres" ]
then
    echo "Waiting for postgres at $POSTGRES_HOST:$POSTGRES_PORT..."
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 1
    done
    echo "PostgreSQL started"
fi

# Run migrations
echo "Applying database migrations..."
python manage.py makemigrations --no-input
python manage.py migrate --no-input

# Start server
exec "$@"