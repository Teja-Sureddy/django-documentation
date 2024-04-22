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

#ENV HOME=/home/ubuntu
#ENV APP_HOME=/home/ubuntu/django-documentation
#RUN mkdir $APP_HOME
#RUN mkdir $APP_HOME/statc
#WORKDIR $APP_HOME

RUN mkdir /app/logs
RUN touch /app/logs/django.log

