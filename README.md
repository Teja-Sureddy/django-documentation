# Django Documentation

|                    |            |
|--------------------|------------|
| **OS**             | Windows    |
| **DB Name**        | my_db      |
| **Project Name**   | my_project |
| **Apps Directory** | my_apps    |


## Setup
```
python manage.py makemigrations
python manage.py migrate
python manage.py add_users
python manage.py add_data
```
<hr>


## Table of Contents

- [Installation](#installation)
- [Create a project](#create-a-project)
- [Create an app](#create-an-app)
- [Configure python interpreter](#configure-python-interpreter)
- [Postgres database setup](#postgres-database-setup)
- [Run the migrations](#run-the-migrations)


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

```
# To see what SQL statements that migration would execute:
python manage.py sqlmigrate <app_name> <migration_name>

# To list all models based on your database
python manage.py inspectdb

python manage.py shell

python manage.py createsuperuser
```


---
## Features
### Views
 - Function-Based View
 - [Class-Based View](my_apps/users/views/profile.py)
 - [Class-Based ListView](my_apps/dashboard/views/data.py)
 - Class-Based TemplateView


### Table of Contents
 - [Middleware](my_apps/middleware.py)
 - [Adapter](my_apps/adapter.py)
 - [backend](my_apps/backend.py)
 - [Authentication](my_project/urls.py)
 - [Groups & Permissions](my_apps/users/utils.py)
 - [Get & Delete Data](my_apps/dashboard/views/data.py)
 - [Post & Put Data](my_apps/dashboard/views/data_modify.py)
 - [Dynamic Form Fields](my_apps/dashboard/forms/full_data.py)
 - [File Manager Access](my_apps/users/views/access_file.py)
 - [File Upload](my_apps/users/views/profile.py)
 - [DRF](my_apps/rest/README.md)
 - [WSS](#WSS)


### WSS

 - Install `channels`(v3) and configure [asgi](my_project/asgi.py) and [settings](my_project/settings.py) files.
 - Follow [consumer](my_apps/notification/consumers.py) and [js](static/js/notification.js).

With Broker like redis:

 - Follow above.
 - Install `channels-redis`(v3) in the project.
 - Install `redis` on windows by following https://developer.redis.com/create/windows/.
 - In wsl, run `sudo service redis-server start`.
