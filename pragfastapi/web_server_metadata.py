## Copyright (c) 2020 mangalbhaskar.
"""FastAPI metadata.

https://fastapi.tiangolo.com/tutorial/metadata/

You don't have to add metadata for all the tags that you use.

Use the tags parameter with your path operations (and APIRouters) to assign them to different tags
https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags

The order of each tag metadata dictionary also defines the order shown in the docs UI.


OpenAPI URL
By default, the OpenAPI schema is served at /openapi.json.

Swagger UI: served at /docs.
You can set its URL with the parameter docs_url.
You can disable it by setting docs_url=None.

ReDoc: served at /redoc.
You can set its URL with the parameter redoc_url.
You can disable it by setting redoc_url=None

https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/
Exclude from OpenAPI¶
To exclude a path operation from the generated OpenAPI schema (and thus, from the automatic documentation systems), use the parameter include_in_schema and set it to False;

You can limit the lines used from the docstring of a path operation function for OpenAPI.

Adding an \f (an escaped "form feed" character) causes FastAPI to truncate the output used for OpenAPI at this point.

It won't show up in the documentation, but other tools (such as Sphinx) will be able to use the rest.

https://fastapi.tiangolo.com/advanced/additional-responses/

https://fastapi.tiangolo.com/advanced/response-directly/
You can override it by returning a Response directly as seen in Return a Response directly.

But if you return a Response directly, the data won't be automatically converted, and the documentation won't be automatically generated (for example, including the specific "media type", in the HTTP header Content-Type as part of the generated OpenAPI).

When you return a Response directly its data is not validated, converted (serialized), nor documented automatically.
But you can still document it as described in Additional Responses in OpenAPI.

If you use a response class with no media type, FastAPI will expect your response to have no content, so it will not document the response format in its generated OpenAPI docs.

https://github.com/ijl/orjson
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


from typing import Optional, Set

from fastapi import FastAPI, Response
from pydantic import BaseModel

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class Item(BaseModel):
  name: str
  description: Optional[str] = None
  price: float
  tax: Optional[float] = None
  tags: Set[str] = []

# app = FastAPI(
#   title="My Super Project",
#   description="This is a very fancy project, with auto docs for the API and everything",
#   version="2.5.0"
# )


# @app.get("/items/")
# async def read_items():
#   return [{"name": "Foo"}]

tags_metadata = [
  {
    "name": "users",
    "description": "Operations with users. The **login** logic is also here.",
  },
  {
    "name": "items",
    "description": "Manage items. So _fancy_ they have their own docs.",
    "externalDocs": {
        "description": "Items external docs",
        "url": "https://fastapi.tiangolo.com/",
    },
  },
]

## If you want to disable the OpenAPI schema completely you can set openapi_url=None, that will also disable the documentation user interfaces that use it.
app = FastAPI(
  title="My Super Project"
  ,description="This is a very fancy project, with auto docs for the API and everything"
  ,version="2.5.0"
  ,openapi_tags=tags_metadata
  ,openapi_url="/api/v1/openapi.json"
  # ,openapi_url=None
  ,docs_url="/documentation"
  # ,docs_url=None
  # ,redoc_url=None
  ,redoc_url="/docs"
)


@app.get("/users/", tags=["users"])
async def get_users():
  return [{"name": "Harry"}, {"name": "Ron"}]


@app.get("/items/", tags=["items"])
async def get_items():
  return [{"name": "wand"}, {"name": "flying broom"}]



@app.get("/exitems/", tags=["exitems"], include_in_schema=False)
async def get_exitems():
  return [{"name": "wand"}, {"name": "flying broom"}]


@app.post("/items/", response_model=Item, summary="Create an item", tags=["items"])
async def create_item(item: Item):
  """
  Create an item with all the information:

  - **name**: each item must have a name
  - **description**: a long description
  - **price**: required
  - **tax**: if the item doesn't have tax, you can omit this
  - **tags**: a set of unique tag strings for this item
  \f
  :param item: User input.
  """
  return item


@app.put("/items/{id}", tags=["items"])
def update_item(id: str, item: Item):
  json_compatible_item_data = jsonable_encoder(item)
  return JSONResponse(content=json_compatible_item_data)


@app.get("/legacy/")
def get_legacy_data():
  data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
  return Response(content=data, media_type="application/xml")
