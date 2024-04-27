# Use the official Python image as a base image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Create a log file
RUN mkdir /app/logs
RUN touch /app/logs/django.log
