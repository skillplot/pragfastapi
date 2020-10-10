## Copyright (c) 2020 mangalbhaskar.
"""FastAPI dependency injection.

https://fastapi.tiangolo.com/tutorial/dependencies/

What is "Dependency Injection"
"Dependency Injection" means, in programming, that there is a way for your code (in this case, your path operation functions) to declare things that it requires to work and use: "dependencies".

And then, that system (in this case FastAPI) will take care of doing whatever is needed to provide your code with those needed dependencies ("inject" the dependencies).

Other common terms for this same idea of "dependency injection" are:

resources
providers
services
injectables
components

Integrations and "plug-in"s can be built using the Dependency Injection system.


The key factor is that a dependency should be a "callable".
A "callable" in Python is anything that Python can "call" like a function.
A Python class is also a callable.
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


from typing import Optional
from fastapi import Cookie, Depends, FastAPI, Header, HTTPException

app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
  def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
    self.q = q
    self.skip = skip
    self.limit = limit


async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
  return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
  return commons


@app.get("/citems/")
# async def read_items(commons: CommonQueryParams = Depends()):
# async def read_items(commons = Depends(CommonQueryParams)):
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response



def query_extractor(q: Optional[str] = None):
  return q


def query_or_cookie_extractor(
  q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)
):
  if not q:
    return last_query
  return q


@app.get("/ditems/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
  return {"q_or_cookie": query_or_default}


## Dependencies in path operation decorators¶
## https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/
## curl -X GET "http://127.0.0.1:8000/token/items" -H  "accept: application/json" -H  "x-token: fake-super-secret-token" -H  "x-key: fake-super-secret-key"

## They can declare request requirements (like headers) or other sub-dependencies:
## These dependencies can raise exceptions, the same as normal dependencies:
## And they can return values or not, the values won't be used.
async def verify_token(x_token: str = Header(...)):
  if x_token != "fake-super-secret-token":
    raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
  if x_key != "fake-super-secret-key":
    raise HTTPException(status_code=400, detail="X-Key header invalid")
  return x_key


## These dependencies will be executed/solved the same way normal dependencies. But their value (if they return any) won't be passed to your path operation function.
@app.get("/token/items", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_token_items():
  return [{"item": "Foo"}, {"item": "Bar"}]
