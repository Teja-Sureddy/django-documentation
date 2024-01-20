# Django Documentation

|                  |                     |
|------------------|---------------------|
| **OS**           | Windows             |
| **DB Name**      | my_db               |
| **Project Name** | my_project          |
| **App Names**    | `my_app1` `my_app2` |


## Table of Contents

- [Installation](#installation)
- [Create a project](#create-a-project)
- [Create an app](#create-an-app)
- [Configure python interpreter](#configure-python-interpreter)
- [Postgres database setup](#postgres-database-setup)
- [Run the migrations](#run-the-migrations)


<hr>


## Installation

Download & install the latest version of `python` from  [this](https://www.python.org/downloads/windows/)
and upgrade the `pip`:

```sh
python -m pip install --upgrade pip
```

Download & install the latest version of `postgres` from [this](https://www.postgresql.org/download/windows/).

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
Create an app names called `my_app1` & `my_app2`:

```sh
python manage.py startapp my_app1
python manage.py startapp my_app2
```

Add `'my_app1.apps.MyApp1Config', 'my_app1.apps.MyApp2Config'` to the `INSTALLED_APPS` in [settings](my_project/settings.py) file and run the [migrations](#run-the-migrations).

## Configure python interpreter

You can configure Python interpreter in your IDE or `command line`:
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

To unapply migrations:

```
python manage.py showmigrations
python manage.py migrate <app_name> zero
```

To see what SQL statements that migration would execute:
```
python manage.py sqlmigrate <app_name> <migration_name>
```

# Application

## Table of Contents

- [CRUD](#crud)
- [Shell](#shell)
- [Django admin](#djando-admin)
- [Debugger](#debugger)
- [Packaging and using your app](#packaging-and-using-your-app)


## CRUD

- Design models as per the [models](my_app1/views.py) and run the [migrations](#run-the-migrations).
- Run the [management commands](my_app1/management/commands/insert_dummy_data.py) to insert data.
    ```s
    python manage.py insert_dummy_data
    ```
- See basic operations from [view](my_app1/views.py) file.


## Shell

```sh 
python manage.py shell
```


## Djando admin

Create a user who can login to the admin site:

```sh
python manage.py createsuperuser
```

Register the models for the my_app1 app in [admin](my_app1/admin.py) file to do the CURD operations from the admin panel.

## Debugger

Follow [this](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html), and it works for the templates containing HTML tags.

## Packaging and using your app

Follow [this](https://docs.djangoproject.com/en/5.0/intro/reusable-apps/#packaging-your-app).

