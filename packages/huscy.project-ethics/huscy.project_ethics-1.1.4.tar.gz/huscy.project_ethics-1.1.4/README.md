huscy.project-ethics
======

![PyPi Version](https://img.shields.io/pypi/v/huscy-project-ethics.svg)
![PyPi Status](https://img.shields.io/pypi/status/huscy-project-ethics)
![PyPI Downloads](https://img.shields.io/pypi/dm/huscy-project-ethics)
![PyPI License](https://img.shields.io/pypi/l/huscy-project-ethics?color=yellow)
![Python Versions](https://img.shields.io/pypi/pyversions/huscy-project-ethics.svg)
![Django Versions](https://img.shields.io/pypi/djversions/huscy-project-ethics)



Requirements
------

- Python 3.6+
- A supported version of Django

Tox tests on Django versions 2.2, 3.1 and 3.2.



Installation
------

To install `husy.project-ethics` simply run:
```
pip install huscy.project-ethics
```



Configuration
------

First of all, the `huscy.project_ethics` application has to be hooked into the project.

1. Add `huscy.project_ethics` and further required apps to `INSTALLED_APPS` in settings module:

```python
INSTALLED_APPS = (
    ...
    'guardian',
    'rest_framework',

    'huscy.project_ethics',
    'huscy.projects',
)
```

2. Create `huscy.project-ethics` database tables by running:

```
python manage.py migrate
```



Development
------

After checking out the repository you should activate any virtual environment.
Install all development and test dependencies:

```
make install
```

Create database tables:

```
make migrate
```

We assume you're having a running postgres database with a user `huscy` and a database also called `huscy`.
You can easily create them by running

```
sudo -u postgres createuser -d huscy
sudo -u postgres createdb huscy
sudo -u postgres psql -c "ALTER DATABASE huscy OWNER TO huscy;"
sudo -u postgres psql -c "ALTER USER huscy WITH PASSWORD '123';"
```
