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
Exclude from OpenAPI
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
orjson is a fast, correct JSON library for Python. It benchmarks as the fastest Python library for JSON and is more correct than the standard json library or other third-party libraries. It serializes dataclass, datetime, numpy, and UUID instances natively.

The ORJSONResponse is currently only available in FastAPI, not in Starlette.

"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


import glob
import time
from typing import Optional, Set

from fastapi import FastAPI, Response
from pydantic import BaseModel

from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse

# from fastapi import staticfiles
from starlette import staticfiles

import pkg_resources

from fastapi.responses import (
    JSONResponse
    ,ORJSONResponse
    ,HTMLResponse
    ,PlainTextResponse
    ,RedirectResponse
    ,StreamingResponse
    ,FileResponse
  )


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


some_file_path = "data/videos/video.mp4"
some_file_path_big = "data/videos/car_parking.mp4"
some_file_path_huge = "data/videos/4k.mp4"
image_basepath = 'data/images'


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
## Even if you uses default_response_class, you can still override response_class in path operations as before.
app = FastAPI(
  title="My Super Project"
  ,description="This is a very fancy project, with auto docs for the API and everything"
  ,version="2.5.0"
  ,openapi_tags=tags_metadata
  ,openapi_url="/api/v1/openapi.json"
  # ,openapi_url=None
  # ,docs_url="/documentation"
  # ,docs_url=None
  # ,redoc_url=None
  # ,redoc_url="/docs"
  ,default_response_class=ORJSONResponse
)

# app.mount("/web", staticfiles.StaticFiles(directory=pkg_resources.resource_filename(__name__, 'app/_site')), name="web")
app.mount("/site", staticfiles.StaticFiles(directory=pkg_resources.resource_filename(__name__, 'app/_site'), html = True), name="site")


@app.get("/.*", include_in_schema=False)
def root():
  return responses.HTMLResponse(pkg_resources.resource_string(__name__, 'app/_site/*'))


@app.get("/hello", response_class=PlainTextResponse)
async def main():
  return "Hello World"


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


@app.get("/orjson_items/", tags=["items"], response_class=ORJSONResponse)
async def read_orjson_items():
  return [{"item_id": "Foo"}]


def generate_html_response():
  html_content = """
  <html>
      <head>
          <title>Some HTML in here</title>
      </head>
      <body>
          <h1>Look ma! HTML!</h1>
      </body>
  </html>
  """
  return HTMLResponse(content=html_content, status_code=200)


@app.get("/html_items/", tags=["items"], response_class=HTMLResponse)
async def read_html_items():
  return generate_html_response()


@app.get("/typer")
async def read_typer():
  return RedirectResponse("https://typer.tiangolo.com")


async def fake_video_streamer():
  for i in range(10):
    yield b"some fake video bytes"


@app.get("/stream", tags=["stream"])
async def stream():
  return StreamingResponse(fake_video_streamer())



## Notice that here as we are using standard open() that doesn't support async and await, we declare the path operation with normal def.
@app.get("/stream/video", tags=["stream"])
def stream_video():
  file_like = open(some_file_path, mode="rb")
  return StreamingResponse(file_like, media_type="video/mp4")


@app.get("/stream/video_async", tags=["stream"])
async def stream_video_async():
  return FileResponse(some_file_path_big, media_type="video/mp4")
  # return FileResponse(some_file_path_big)


@app.get("/stream/video_4k", tags=["stream"])
async def stream_video_async_4k():
  return FileResponse(some_file_path_huge, media_type="video/mp4")
  # return FileResponse(some_file_path_huge)


@app.get("/stream/images", tags=["stream"])
async def stream_image():
  # for f in get_frame():
  #   print("file: {}".format(f))
  #   # return FileResponse(f)
  #   # return StreamingResponse(f)
  #   # return StreamingResponse(f, media_type='multipart/x-mixed-replace; boundary=frame')
  return StreamingResponse(get_frame(), media_type='multipart/x-mixed-replace; boundary=frame')
  # return FileResponse(f)


# async def get_image_filepath():
#   imagelist = glob.glob(image_basepath+'**/*.*')
#   for filepath in imagelist:
#     time.sleep(2)
#     yield filepath


def get_frame():
  imagelist = glob.glob(image_basepath+'**/*.*')
  for f in imagelist:
    frame = open(f, 'rb').read()
    time.sleep(2)
    # yield frame
    yield (b'--frame\r\n' b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')
    # yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == '__main__':
  print(imagelist)
  for i in get_frame():
    print(i)
