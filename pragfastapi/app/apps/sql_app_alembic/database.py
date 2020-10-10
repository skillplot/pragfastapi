"""Database interaction using sqlalchemy ORM.

https://fastapi.tiangolo.com/tutorial/sql-databases
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker


## adapt it with your database data and credentials (equivalently for MySQL, MariaDB or any other)
DATABASE_URI = "sqlite:///./sql_app.db"
# DATABASE_URI = "postgresql://user:password@postgresserver/db"

## connect_args={"check_same_thread": False} is needed only for SQLite DB and not for other databases
## By default SQLite will only allow one thread to communicate with it, assuming that each thread would handle an independent request.
## This is to prevent accidentally sharing the same connection for different things (for different requests).
## But in FastAPI, using normal functions (def) more than one thread could interact with the database for the same request, so we need to make SQLite know that it should allow that with connect_args={"check_same_thread": False}.
## Also, we will make sure each request gets its own database connection session in a dependency, so there's no need for that default mechanism.
engine = create_engine(
  DATABASE_URI
  ,connect_args={
    'check_same_thread': False
  }
)

## Each instance of the DBSession class will be a database session. The class itself is not a database session yet.
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class CustomBase(object):
    ## Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

## Later we will inherit from Base class to create each of the database models or classes (the ORM models):
# Base = declarative_base()
Base = declarative_base(cls=CustomBase)
