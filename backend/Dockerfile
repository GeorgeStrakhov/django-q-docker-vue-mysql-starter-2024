FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install system dependencies
# Install netcat for checking MySQL availability
RUN apt-get update && \
    apt-get install -y supervisor && \
    apt-get install -y netcat-traditional && \
    apt-get install -y default-libmysqlclient-dev build-essential pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# make startup script executable
RUN chmod +x /app/app/startup.sh

# prep supervisord - it runs qcluster on prod
COPY supervisord.conf /etc/supervisor/conf.d/
RUN chmod +x /etc/supervisor/conf.d/supervisord.conf

# Define environment variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# this is only a fallback if the entrypoint is not set for some reason
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

