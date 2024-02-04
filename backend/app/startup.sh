#!/bin/bash

# MySQL host and port
MYSQL_HOST=db  # or the name of your MySQL service in docker-compose
MYSQL_PORT=3306 # default MySQL port

# Wait for MySQL
echo "Waiting for MySQL to be ready..."
while ! nc -z $MYSQL_HOST $MYSQL_PORT; do
  sleep 1 # wait for 1 second before checking again
done

echo "MySQL is up - executing command"

# Apply database migrations and create superuser
python manage.py migrate
python create_superuser.py

# collect static files if not already collected
if [ -d "staticfiles" ]; then
    echo "Static files already collected"
else
    python manage.py collectstatic
fi

# Decide which server to run based on the ENV variable
if [ "$ENV" = "development" ]; then
    echo "Starting Django development server"
    python manage.py runserver 0.0.0.0:8000 &
    python watch.py #ensures livereload is running for qcluster tasks
else
    echo "Starting supervisor to start guvicorn and qcluster"
    supervisord -c /etc/supervisor/conf.d/supervisord.conf
fi
