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


JSON Compatible Encoder
https://fastapi.tiangolo.com/tutorial/encoder/
There are some cases where you might need to convert a data type (like a Pydantic model) to something compatible with JSON (like a dict, list, etc).
jsonable_encoder is actually used by FastAPI internally to convert data. But it is useful in many other scenarios.

https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT
https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH
partial update - This means that you can send only the data that you want to update, leaving the rest intact.
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


from typing import List, Optional, Set, Dict
import uuid

import fastapi
from fastapi import Body
from fastapi.encoders import jsonable_encoder

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
  email: str
  alternate_email: Optional[str] = None
  hashed_password: str
  is_active: Optional[bool] = True
  is_superuser: Optional[bool] = False
  disabled: Optional[bool] = None



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


fake_db = {}

app = fastapi.FastAPI()


@app.post('/hello/')
async def hello_user(user: User):
  return user


@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    - **images**: list of item images
    """
    return item


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
  # json_compatible_item_data = jsonable_encoder(item)
  json_compatible_item_data = jsonable_encoder(results)
  fake_db[item_id] = json_compatible_item_data
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
