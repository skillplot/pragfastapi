## Copyright (c) 2020 mangalbhaskar.
"""user-item web server.

https://fastapi.tiangolo.com/tutorial/sql-databases

Notice that the values you return are SQLAlchemy models, or lists of SQLAlchemy models.

But as all the path operations have a response_model with Pydantic models / schemas using orm_mode, the data declared in your Pydantic models will be extracted from them and returned to the client, with all the normal filtering and validation

Also notice that there are response_models that have standard Python types like List[schemas.Item].

But as the content/parameter of that List is a Pydantic model with orm_mode, the data will be retrieved and returned to the client as normally, without problems.


And as the code related to SQLAlchemy and the SQLAlchemy models lives in separate independent files, you would even be able to perform the migrations with Alembic without having to install FastAPI, Pydantic, or anything else.

The same way, you would be able to use the same SQLAlchemy models and utilities in other parts of your code that are not related to FastAPI.
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


import platform
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


if float('.'.join(platform.python_version_tuple()[:-1])) == 3.6:
  from fastapi import Request, Response

  @app.middleware("http")
  async def db_session_middleware(request: Request, call_next):
    """Alternative DB session with middleware
    If you can't use dependencies with yield -- for example, if you are not using Python 3.7 and can't install the "backports" mentioned above for Python 3.6 -- you can set up the session in a "middleware" in a similar way.

    A "middleware" is basically a function that is always executed for each request, with some code executed before, and some code executed after the endpoint function."""
    response = Response("Internal server error", status_code=500)
    try:
      request.state.db = database.DBSession()
      response = await call_next(request)
    finally:
      request.state.db.close()
    return response


  # Dependency
  def get_db(request: Request):
    return request.state.db

else:
  ## Dependency
  def get_db():
    db = database.DBSession()
    try:
      yield db
    finally:
      db.close()


## create user
@app.post("/users/", response_model=schemas.User)
def create_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
  db_user = crud.get_user_by_email(db, email=user.email)
  if db_user:
    raise HTTPException(status_code=400, detail="Email already registered")
  return crud.create_user(db=db, user=user)


## read users
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip:int=0, limit:int=100, db:Session=Depends(get_db)):
  users = crud.get_users(db, skip=skip, limit=limit)
  return users


## read user
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id:int, db:Session=Depends(get_db)):
  db_user = crud.get_user(db, user_id=user_id)
  if db_user is None:
    raise HTTPException(status_code=404, detail='User not found')
  return db_user


## create item for user
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
  user_id:int
  ,item:schemas.ItemCreate
  ,db:Session=Depends(get_db)):
  return crud.create_user_item(db=db, item=item, user_id=user_id)


## read items
@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip:int=0, limit:int=100, db:Session=Depends(get_db)):
  items = crud.get_items(db, skip=skip, limit=limit)
  return items
