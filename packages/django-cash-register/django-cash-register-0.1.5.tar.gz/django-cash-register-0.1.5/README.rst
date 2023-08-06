===============
DJANGO SHOP APP
===============

django-cash-register is a Django app to manage product by cashier.

Installation
============
::

    pip install django-cash-register

Quick start
===========

1. Add "django_cash_register" to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        ...
        'django_cash_register',
    ]

2. Execute command::

    ./manage.py migrate

3. Start the development server and visit http://127.0.0.1:8000/admin