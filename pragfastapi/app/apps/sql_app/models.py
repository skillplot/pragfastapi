## Copyright (c) 2020 mangalbhaskar.
"""Database interaction using sqlalchemy ORM.

https://fastapi.tiangolo.com/tutorial/sql-databases

SQLAlchemy and many others are by default "lazy loading".
That means, for example, that they don't fetch the data for relationships from the database unless you try to access the attribute that would contain that data.

https://stackoverflow.com/questions/183042/how-can-i-use-uuids-in-sqlalchemy
https://stackoverflow.com/questions/36806403/cant-render-element-of-type-class-sqlalchemy-dialects-postgresql-base-uuid#36820005
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import UUID

from .database import Base


class User(Base):
  """SQLAlchemy User model definition."""

  ## For postgresql
  # uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, index=True)
  ## For sqlite
  uuid = Column(Text(length=36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True)
  id = Column(Integer, primary_key=True, nullable=False, index=True)
  full_name = Column(String, nullable=False, index=True)
  username = Column(String, unique=True, nullable=False, index=True)
  email = Column(String, unique=True, nullable=False, index=True)
  alternate_email = Column(String, unique=True, nullable=False, index=True)
  hashed_password = Column(String, nullable=False)
  is_active = Column(Boolean, default=True, nullable=False)
  is_superuser = Column(Boolean, default=False, nullable=False)

  items = relationship("Item", back_populates="owner")


class Item(Base):
  """SQLAlchemy User model definition."""

  uuid = Column(Text(length=36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True)
  id = Column(Integer, primary_key=True, nullable=False, index=True)
  title = Column(String, index=True, nullable=False, index=True)
  description = Column(String, index=True)
  owner_id = Column(Integer, ForeignKey("user.id"))

  owner = relationship("User", back_populates="items")
