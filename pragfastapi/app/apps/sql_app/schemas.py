## Copyright (c) 2020 mangalbhaskar.
"""The Pydantic models.

Create Pydantic models / schemas for reading / returning


https://fastapi.tiangolo.com/tutorial/sql-databases

To avoid confusion between the SQLAlchemy models and the Pydantic models, we will have the file models.py with the SQLAlchemy models, and the file schemas.py with the Pydantic models.
These Pydantic models define more or less a "schema" (a valid data shape).
So this will help us avoiding confusion while using both.


Notice that the User, the Pydantic model that will be used when reading a user (returning it from the API) doesn't include the password.

Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).

Without orm_mode, if you returned a SQLAlchemy model from your path operation, it wouldn't include the relationship data. Even if you declared those relationships in your Pydantic models.
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com github.com/dmontagu'


import re

from functools import partial
from typing import Any, Dict, List, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseConfig, BaseModel


def snake2camel(snake: str, start_lower: bool = False) -> str:
  camel = snake.title()
  camel = re.sub("([0-9A-Za-z])_(?=[0-9A-Z])", lambda m: m.group(1), camel)
  if start_lower:
      camel = re.sub("(^_*[A-Z])", lambda m: m.group(1).lower(), camel)
  return camel


class APIModel(BaseModel):
  class Config(BaseConfig):
      orm_mode = True
      allow_population_by_alias = True
      alias_generator = partial(snake2camel, start_lower=True)

  def dump_obj(self, **jsonable_encoder_kwargs: Any) -> Dict[str, Any]:
      return jsonable_encoder(self, **jsonable_encoder_kwargs)


class ItemBase(APIModel):
  title: str
  description: Optional[str] = None


class ItemCreate(ItemBase):
  pass

class Item(ItemBase):
  id: int
  owner_id: int


class UserBase(APIModel):
  full_name: str
  primary_email: str
  alternate_email: Optional[str]


## Properties to receive via API on creation
class UserCreate(UserBase):
  password: str


## Properties to receive via API on update
class UserUpdate(UserBase):
  password: Optional[str] = None
  alternate_email: Optional[str] = None


## Additional properties to return via API
class User(UserBase):
  id: int
  is_active: bool
  items: List[Item] = []
