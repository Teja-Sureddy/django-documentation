# Django Documentation

You will find almost everything about django here, along with the usage of several popular packages, deployment, ...


## Table of Contents

 - [Local Initial Setup](#local-initial-setup)
 - [Setup from Scratch](#setup-from-scratch)
 - [Docker Setup](#docker-setup)
 - [Infrastructure Setup & Build](#infrastructure-setup--build)
 - [Django Features](#django-features)



---
# Local Initial Setup

## With Docker

Install Docker desktop and run,

```
docker-compose up --build
docker-compose exec django python manage.py add_users
docker-compose exec django python manage.py add_data
docker-compose exec django python manage.py add_notifications
docker-compose exec django python manage.py add_invoices
```


## Without Docker

Setup python virtual environment and run,

```
pip install -r requirements.txt
```

```
python manage.py migrate
python manage.py add_users
python manage.py add_data
python manage.py add_notifications
python manage.py add_invoices
```



---
# Setup from Scratch

## Table of Contents

- [Installation](#installation)
- [Create a project](#create-a-project)
- [Create an app](#create-an-app)
- [Configure python interpreter](#configure-python-interpreter)
- [Postgres database setup](#postgres-database-setup)
- [Run the migrations](#run-the-migrations)
- [Other Commands](#other-commands)


## Installation

Download & install the latest version of `python` from  [link](https://www.python.org/downloads/windows/)
and upgrade the `pip`:

```sh
python -m pip install --upgrade pip
```

Download & install the latest version of `postgres` from [link](https://www.postgresql.org/download/windows/).

Install django globally:

```sh
python -m pip install Django
```

Check the version:

```sh
python -m django --version
```


## Create a project

Start a new django project called `my_project`:

```sh
django-admin startproject my_project
```

Run the server for testing (`8000` is optional):

```sh
python manage.py runserver 8000
```


## Create an app

There is no limitation of creating number of apps in django.<br>
Create an app name called `users` & `dashboard`:

```sh
python manage.py startapp users
python manage.py startapp dashboard
```

Add `'users', 'dashboard'` to the `INSTALLED_APPS` in [settings](my_project/settings.py) file and run the [migrations](#run-the-migrations).

## Configure python interpreter

You can configure Python interpreter from your IDE or `command line`:
```sh
python -m venv venv
.\venv\Scripts\activate
```

Create a [requirements](requirements.txt) file in the root directory,
and list the packages inside it and install them:
```sh
pip install -r requirements.txt
```


## Postgres database setup

Create a database called `my_db` and
Install `psycopg2` package.<br>
Open up the [settings](my_project/settings.py) file and add the below config to the `DATABASES`:

```
'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'my_db',
    'USER': 'postgres',
    'PASSWORD': 'admin',
    'HOST': 'localhost',
    'PORT': '5432'
}
```


## Run the migrations

Run the migrations when the `database config` or a `model` is modified:

```sh
python manage.py makemigrations
python manage.py migrate
```

To remove migrations:

```
python manage.py showmigrations
python manage.py migrate <app_name> zero
```


## Other Commands

| Command                                                   | Description                                                            |
|-----------------------------------------------------------|------------------------------------------------------------------------|
| `python manage.py createsuperuser`                        | Creates a superuser for the admin interface.                           |
| `python manage.py shell`                                  | Opens an interactive Python shell with Django settings loaded.         |
| `python manage.py sqlmigrate <app_name> <migration_name>` | Shows the SQL statements for a migration.                              |
| `python manage.py inspectdb`                              | Generates model code by inspecting the database.                       |
| `python manage.py collectstatic`                          | Collects static files into `STATIC_ROOT` for production use.           |
| `python manage.py check`                                  | Checks the entire Django project for potential issues.                 |
| `python manage.py test`                                   | Runs the test suite for the project.                                   |
| `python manage.py flush`                                  | Deletes all data in the database and reloads initial data.             |
| `python manage.py loaddata <fixture>`                     | Loads data from fixture files into the database.                       |
| `python manage.py dumpdata <app_name>`                    | Outputs data from the database as a fixture (e.g., JSON, XML).         |
| `python manage.py showmigrations`                         | Lists all migrations and their status.                                 |
| `python manage.py dbshell`                                | Opens the database shell.                                              |
| `python manage.py diffsettings`                           | Displays differences between the current settings and Django defaults. |
| `python manage.py sendtestemail`                          | Sends a test email to ensure email settings are correct.               |
| `python manage.py changepassword <username>`              | Changes the password for the specified user.                           |
| `python manage.py clearsessions`                          | Removes expired sessions from the database.                            |



---
# Docker Setup

 - Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
 - Create `Dockerfile`, `.dockerignore` and `docker-compose.yml` files.
 - To build and run `docker-compose up --build`.
 - To manually run a command `docker-compose exec <service_name> python manage.py <cmd>`

You can manage things in docker desktop or by below commands,

```
docker-compose build
docker-compose up -d  # creates and starts containers
docker-compose down  # stop and remove containers
docker-compose start, stop, restart, pause, unpause, kill, logs -f

For a particular service,
docker-compose start <service_name>

docker-compose exec <service> <command>  # Execute a command in a running service container
docker-compose run <service> <command>  # Run a one-off command in a new container

docker rm -f $(docker ps -aq)  # Delete all containers
docker rmi -f $(docker images -aq)  # Delete all images
docker-compose rm -f <service_name>  # Delete a particular container
docker rmi <image_name_or_id>  # Delete a particular image

docker volume ls  # List all volumes
docker volume rm <volumn_name>  # Delete particular volume
docker volume prune   # Delete all volume
```

There are two commands: `docker-compose` (which needs separate installation) and `docker compose` (which comes with the Docker CLI). They both serve the same purpose.



---
# Infrastructure Setup & Build

 - [Build](infrastructure/build/README.md)
 - [One-Time Setup](infrastructure/setup/setup.sh)



---
# Django Features

## Table of Contents

 - [Views](#views)
 - [Middleware](my_apps/middleware.py)
 - [Adapter](my_apps/adapter.py)
 - [Backend](my_apps/backend.py)
 - [Signals](my_apps/users/signals.py)
 - [Authentication](my_project/urls.py)
 - [Groups & Permissions](my_apps/users/utils.py)
 - [ORM](my_apps/dashboard/README.md)
 - [Get & Delete Data](my_apps/dashboard/views/data.py)
 - [Post & Put Data](my_apps/dashboard/views/data_modify.py)
 - [Dynamic Form Fields](my_apps/dashboard/forms/full_data.py)
 - [File Manager Access](my_apps/users/views/access_file.py)
 - [File Upload](my_apps/users/views/profile.py)
 - [DRF](my_apps/rest/README.md)
 - [WSS](#WSS)
 - [Background task](my_apps/background_task/README.md)
 - [PDF - Generate / Process](my_apps/pdf/__init__.py)


### Views

`Function-Based View`, [Class-Based View](my_apps/users/views/profile.py), [Class-Based ListView](my_apps/dashboard/views/data.py) and `Class-Based TemplateView`.


### WSS

 - Install `channels`(v3) and configure [asgi](my_project/asgi.py) and [settings](my_project/settings.py) files.
 - Follow [consumer](my_apps/notification/consumers.py) and [js](static/js/notification.js).

With Broker like redis, additionally:

 - Install `channels-redis`(v3) in the project.
 - Install `redis` on windows by following https://developer.redis.com/create/windows/.
 - In wsl, run `sudo service redis-server start`.


### Logging
```
import logging
logger = logging.getLogger(__name__)

logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
```

### Code Coverage

```
pre-commit install
```
