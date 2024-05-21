# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Install RabbitMQ and SQLite3 packages
RUN apt-get update && apt-get install -y \
    rabbitmq-server \
    sqlite3

# Expose RabbitMQ default port and management UI port
EXPOSE 5672 15672

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "/src/app.py"]


