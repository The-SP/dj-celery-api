#!/bin/bash

# Change to the backend directory
cd backend

# Wait for database to be ready
if [ "$DATABASE_HOST" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
        sleep 0.1
    done
    echo "PostgreSQL started"
fi

# Run migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Start server
exec "$@"