## Copyright (c) 2020 mangalbhaskar.
"""FastAPI hello-world application server.

https://fastapi.tiangolo.com/tutorial/body/

https://fastapi.tiangolo.com/tutorial/body-nested-models/

But with all the benefits:

Editor support (completion everywhere!)
Data conversion (a.k.a. parsing / serialization)
Data validation
Schema documentation
Automatic docs

https://pydantic-docs.helpmanual.io/usage/schema/#schema-customization

"""
__author__ = 'mangalbhaskar'


from typing import List, Optional, Set, Dict
import uuid

import fastapi
from fastapi import Body, Cookie
from pydantic import BaseModel, Field, HttpUrl

from app.dnn import dnnarch


ItemExample = {
  "name": "Foo",
  "description": "A very nice Item",
  "price": 35.4,
  "tax": 3.2,
}

class Image(BaseModel):
  # url: str
  url: HttpUrl
  name: str


class User(BaseModel):
  uuid: str = lambda: str(uuid.uuid4())
  full_name: str
  primary_email: str
  alternate_email: Optional[str] = None
  hashed_password: str
  is_active: bool = True
  is_superuser: bool = False


class Item(BaseModel):
  name: str
  description: Optional[str] = Field(
      None, title="The description of the item", max_length=300
  )
  price: float = Field(..., gt=0, description="The price must be greater than zero")
  tax: Optional[float] = None
  # tags: list = []
  # tags: List[str] = []
  tags: Set[str] = []
  # image: Optional[Image] = None
  images: Optional[List[Image]] = None

  class Config:
    schema_extra = {
      "example": ItemExample
    }


class Offer(BaseModel):
  name: str
  description: Optional[str] = None
  price: float
  items: List[Item]


app = fastapi.FastAPI()


@app.get("/cookie/")
async def eat_cookie(ads_id: Optional[str] = Cookie(None)):
  return {"ads_id": ads_id}


@app.post('/hello/')
async def hello_user(user: User):
  return user


@app.put("/items/{item_id}")
async def update_item(
  item_id:int
  ,item:Item
  ,user:User
  ## But you can instruct FastAPI to treat it as another body key using Body
  ## Body also has all the same extra validation and metadata parameters as Query,Path and others.
  ,importance:int=Body(...)
  ):
  results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
  return results


@app.post("/offers/")
async def create_offer(offer: Offer):
  return offer


@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
  return images


## Have in mind that JSON only supports str as keys.
## But Pydantic has automatic data conversion.
## This means that, even though your API clients can only send strings as keys, as long as those strings contain pure integers, Pydantic will convert them and validate them.
## And the dict you receive as weights will actually have int keys and float values.
@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
  return weights


@app.get('/')
async def hello_world():
  return {'message':'Hello World!'}


@app.get('/hello/blah')
async def hello_blah():

  return {'message':'Hello {}!'.format('blah')}

@app.get('/hello')
@app.get('/hello/')
@app.get('/hello/{name}')
@app.get('/hello/{name}/age/{age}')
async def hello(
    name: Optional[str] = 'World'
    ,age: Optional[int] = 99
  ):
  return {'message':'Hello {}, your age is {}!'.format(name, age)}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# @app.get('/dnnarch')
# async def dnnarch_query(skip:int=0, limit:int=len(list(dnnarch.DnnArch))):
#   all_dnnarch = [el.name for el in dnnarch.DnnArch][skip: skip+limit]
#   msg = {'message':'dnnarch supported are: {}'.format(all_dnnarch)}
#   return msg


# @app.get('/dnnarch/all')
# async def dnnarch_all():
#   all_dnnarch = [el.name for el in dnnarch.DnnArch]
#   msg = {'message':'dnnarch supported are: {}'.format(all_dnnarch)}
#   return msg


@app.get('/dnnarch')
@app.get('/dnnarch/{name}')
async def dnnarch_type(
    name: Optional[dnnarch.DnnArch] = None
    ,skip: int = 0
    ,limit: int = len(list(dnnarch.DnnArch))
    ,debug: bool = False
  ):
  msg = {'message': None}
  if not name:
    all_dnnarch = [el.name for el in dnnarch.DnnArch][skip: skip+limit]
    msg = {'message':'dnnarch supported are: {}'.format(all_dnnarch)}
  elif name in dnnarch.DnnArch:
    msg = {'message':'dnnarch - {} is supported.'.format(dnnarch.DnnArch[name])}
  if debug:
    print('msg: {}'.format(msg))
  return msg
