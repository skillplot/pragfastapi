# SQL Databases

```bash
pip install SQLAlchemy
pip install async-exit-stack async-generator
```

* Normally you would probably initialize your database (create tables, etc) with Alembic. And you would also use Alembic for "migrations" (that's its main job). A "migration" is the set of steps needed whenever you change the structure of your SQLAlchemy models, add a new attribute, etc. to replicate those changes in the database, add a new column, a new table, etc.

* We need to have an independent database session/connection (SessionLocal) per request, use the same session through all the request and then close it after the request is finished.

* https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/

* https://github.com/sorcio/async_exit_stack
* https://github.com/python-trio/async_generator


https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
What are "Context Managers"
"Context Managers" are any of those Python objects that you can use in a with statement.

When you create a dependency with yield, FastAPI will internally convert it to a context manager, and combine it with some other related tools.


https://docs.python.org/3/reference/datamodel.html#context-managers

https://sqlitebrowser.org/
https://dbhub.io/

## Async

* https://fastapi.tiangolo.com/async/#very-technical-details


## Async SQL

* https://fastapi.tiangolo.com/advanced/async-sql-databases/
* https://github.com/encode/databases
* https://www.starlette.io/database/


It is compatible with:

PostgreSQL
MySQL
SQLite


## Alembic

* https://alembic.sqlalchemy.org/

```bash
alembic init alembic

```


## Background task worker


* http://www.celeryproject.org/
* https://python-rq.org/
* https://arq-docs.helpmanual.io/


## Install Python

https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/

https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa

```bash
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt -y install python3.7
python3.7 --version

python3.3 -m venv --upgrade ENV_DIR
python3.7 -m venv ENV_DIR
```

Updating repository keys

https://nvidia.github.io/libnvidia-container/

curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo apt-key add


https://qgis.org/debian/dists/bionic/Release.gpg

wget -O - https://qgis.org/debian/dists/bionic/Release.gpg | gpg --import

curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo apt-key add 


https://github.com/tiangolo/fastapi/issues/413

https://www.starlette.io/requests/#other-state


