## Copyright (c) 2020 mangalbhaskar.
"""FastAPI hello-world application server.

https://fastapi.tiangolo.com/features/
https://github.com/OAI/OpenAPI-Specification
http://json-schema.org/
https://github.com/swagger-api/swagger-ui
https://github.com/Rebilly/ReDoc

https://fastapi.tiangolo.com/python-types/

https://fastapi.tiangolo.com/tutorial/first-steps/
Operation
"Operation" here refers to one of the HTTP "methods".

One of:

POST: to create data.
GET: to read data.
PUT: to update data.
DELETE: to delete data.
...and the more exotic ones:
OPTIONS
HEAD
PATCH
TRACE

That @something syntax in Python is called a "decorator". A "decorator" takes the function below and does something with it.

You can also use the other operations:

@app.post()
@app.put()
@app.delete()
And the more exotic ones:

@app.options()
@app.head()
@app.patch()
@app.trace()

https://fastapi.tiangolo.com/tutorial/path-params/#predefined-values

## Query Parameters and String Validations
https://fastapi.tiangolo.com/tutorial/query-params-str-validations/

You can declare additional validations and metadata for your parameters.

Generic validations and metadata:

alias
title
description
deprecated
Validations specific for strings:

min_length
max_length
regex


## Path Parameters and Numeric Validations
https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/
With Query, Path (and others you haven't seen yet) you can declare metadata and string validations

And you can also declare numeric validations:

gt: greater than
ge: greater than or equal
lt: less than
le: less than or equal

Query, Path and others you will see later subclasses of a common Param class (that you don't need to use).

When you import Query, Path and others from fastapi, they are actually functions.
That when called, return instances of classes of the same name.
So, you import Query, which is a function. And when you call it, it returns an instance of a class also named Query.
These functions are there (instead of just using the classes directly) so that your editor doesn't mark errors about their types.
That way you can use your normal editor and coding tools without having to add custom configurations to disregard those errors.

"""
__author__ = 'mangalbhaskar'


from typing import Optional

import fastapi
from fastapi import Path, Query

from app.dnn import dnnarch


app = fastapi.FastAPI()


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
    ## simple without validation
    name: Optional[str] = 'World'
    ,age: Optional[int] = 99
    ,weight: Optional[int] = Path(..., title="Weight of the person", gt=20, le=999)
    ## https://fastapi.tiangolo.com/tutorial/query-params-str-validations/
    ,q: Optional[str] = Query(
      'Deep Learning'
      ,title='Query String'
      ,min_length=3
      ,max_length=50
      ,regex='[a-zA-Z]+'
    )
    ,mq: Optional[list] = Query(
      ## Using list
      ['blah', 'dummy']
      ## Declare more metadata
      ,title='Multiple Query String'
      ,description='Search for more then one query term.'
      ## Alias parameters
      ,alias='multi-query'
      ## Deprecating parameters
      ,deprecated=True
    )
  ):
  return {
    'message':
      'Hello {}, your age is {}.\n \
      You queried for: {} and multiple terms: {}!'
      .format(name, age, q, mq)
    }


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
