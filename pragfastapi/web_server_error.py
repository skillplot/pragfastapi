## Copyright (c) 2020 mangalbhaskar.
"""FastAPI Error Handling

https://fastapi.tiangolo.com/tutorial/handling-errors/
https://www.starlette.io/exceptions/

You could also use from starlette.requests import Request and from starlette.responses import JSONResponse.

FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette. The same with Request.
FastAPI has some default exception handlers.
These handlers are in charge of returning the default JSON responses when you raise an HTTPException and when the request has invalid data.
You can override these exception handlers with your own.

https://pydantic-docs.helpmanual.io/#error-handling

You could also use from starlette.responses import PlainTextResponse.

The RequestValidationError contains the body it received with invalid data.
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from pydantic import BaseModel


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


class Item(BaseModel):
    title: str
    size: int


app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.post(
  "/items/"
  ,response_model=Item
  ,summary="Create an item"
  ,response_description="The created item"
  )
async def create_item(item: Item):
  """
  Create an item with all the information:

  - **title**: each item must have a title
  - **size**: size of an item
  """
  return item


@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
  if item_id not in items:
    raise HTTPException(
      status_code=404,
      detail="Item not found",
      headers={"X-Error": "There goes my error"},
    )
  return {"item": items[item_id]}


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
  return JSONResponse(
    status_code=418,
    content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
  )


# ## Use the RequestValidationError body
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#   return JSONResponse(
#     status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#     content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
#   )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
  if name == "yolo":
    raise UnicornException(name=name)
  return {"unicorn_name": name}


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
  return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
  return PlainTextResponse(str(exc), status_code=400)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
  if item_id == 3:
    raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
  return {"item_id": item_id}
