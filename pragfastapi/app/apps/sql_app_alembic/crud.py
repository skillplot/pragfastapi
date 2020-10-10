"""CRUD utility.

CRUD: Create, Read, Update, and Delete.

This example is not secure, the password is not hashed.
In a real life application you would need to hash the password and never save them in plaintext.
Here we are focusing only on the tools and mechanics of databases.

https://fastapi.tiangolo.com/tutorial/sql-databases
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


import uuid
from sqlalchemy.orm import Session

from . import models, schemas

def get_user(db: Session, user_id: int):
  return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
  return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int=0, limit:int=100):
  return db.query(models.User).offset(skip).limit(limit).all()


## The SQLAlchemy model for User contains a hashed_password that should contain a secure hashed version of the password.
## But as what the API client provides is the original password, you need to extract it and generate the hashed password in your application.
## And then pass the hashed_password argument with the value to save.
def create_user(db: Session, user: schemas.UserCreate):
  fake_hased_password = user.password + 'notreallyhashed'
  db_user = models.User(email=user.email, hashed_password=fake_hased_password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

##---

def get_items(db: Session, skip:int=0, limit:int=100):
  return db.query(models.Item).offset(skip).limit(limit).all()


## Instead of passing each of the keyword arguments to Item and reading each one of them from the Pydantic model, we are generating a dict with the Pydantic model's data with:
## item.dict()
## and then we are passing the dict's key-value pairs as the keyword arguments to the SQLAlchemy Item, with:
## Item(**item.dict())
## And then we pass the extra keyword argument owner_id that is not provided by the Pydantic model, with:
## Item(**item.dict(), owner_id=user_id)
def create_user_item(db: Session, item:schemas.ItemCreate, user_id:int):
  d = item.dict()
  print("item: {}, type: {}".format(d, type(d)))
  db_item = models.Item(**d, owner_id=user_id)
  db.add(db_item)
  db.commit()
  db.refresh(db_item)
  return db_item
