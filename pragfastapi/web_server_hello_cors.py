## Copyright (c) 2020 mangalbhaskar.
"""FastAPI hello-world application server.

CORS (Cross-Origin Resource Sharing)
https://fastapi.tiangolo.com/tutorial/cors/
https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

You could also use from starlette.middleware.cors import CORSMiddleware.

FastAPI provides several middlewares in fastapi.middleware just as a convenience for you, the developer. But most of the available middlewares come directly from Starlette.
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


from typing import Optional

import fastapi
from fastapi.middleware.cors import CORSMiddleware

from app.dnn import dnnarch


app = fastapi.FastAPI()

##  A list of origins that should be permitted to make cross-origin requests.
origins = [
  "http://localhost"
  ,"http://localhost:8080"
  ,"http://127.0.0.1:8080"
]

## to allow any origin
# origins = ['*']

app.add_middleware(
  CORSMiddleware
  ## A list of origins that should be permitted to make cross-origin requests.
  ,allow_origins=origins
   ## Indicate that cookies should be supported for cross-origin requests. Defaults to False.
   ##A regex string to match against origins that should be permitted to make cross-origin requests. eg. 'https://.*\.example\.org'.
  # ,allow_origin_regex='https://.*\.example\.org'
  ,allow_credentials=True
  ## A list of HTTP methods that should be allowed for cross-origin requests. Defaults to ['GET']. You can use ['*'] to allow all standard methods.
  ,allow_methods=['*']
   ## A list of HTTP request headers that should be supported for cross-origin requests. Defaults to []. You can use ['*'] to allow all headers. The Accept, Accept-Language, Content-Language and Content-Type headers are always allowed for CORS requests.
  ,allow_headers=['*']
  ## Indicate any response headers that should be made accessible to the browser. Defaults to []
  # ,expose_headers=[]
  ## max_age - Sets a maximum time in seconds for browsers to cache CORS responses. Defaults to 600
  # ,max_age=500
)



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
