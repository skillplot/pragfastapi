## Copyright (c) 2020 mangalbhaskar.
"""FastAPI testing.

https://fastapi.tiangolo.com/tutorial/testing/
https://www.starlette.io/testclient/
http://docs.python-requests.org/
https://docs.pytest.org/

Create a TestClient passing to it your FastAPI.
Create functions with a name that starts with test_ (this is standard pytest conventions).

Notice that the testing functions are normal def, not async def.
And the calls to the client are also normal calls, not using await.
This allows you to use pytest directly without complications.

If you want to call async functions in your tests apart from sending requests to your FastAPI application (e.g. asynchronous database functions), have a look at the Async Tests in the advanced tutorial.
https://fastapi.tiangolo.com/advanced/async-tests/


https://fastapi.tiangolo.com/advanced/testing-websockets/
https://www.starlette.io/testclient/#testing-websocket-sessions

"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


from fastapi import FastAPI

from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from fastapi.websockets import WebSocket


class Item(BaseModel):
  id: str
  title: str
  description: Optional[str] = None


fake_secret_token = "coneofsilence"

fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}

items = {}

app = FastAPI()


@app.get("/")
async def read_main():
  return {"msg": "Hello World"}


@app.get("/items/{item_id}", response_model=Item)
async def read_main(item_id: str, x_token: str = Header(...)):
  if x_token != fake_secret_token:
    raise HTTPException(status_code=400, detail="Invalid X-Token header")
  if item_id not in fake_db:
    raise HTTPException(status_code=404, detail="Item not found")
  return fake_db[item_id]


@app.post("/items/", response_model=Item)
async def create_item(item: Item, x_token: str = Header(...)):
  if x_token != fake_secret_token:
    raise HTTPException(status_code=400, detail="Invalid X-Token header")
  if item.id in fake_db:
    raise HTTPException(status_code=400, detail="Item already exists")
  fake_db[item.id] = item
  return item

@app.get("/titems/{item_id}")
async def read_titems(item_id: str):
  return items[item_id]


@app.websocket_route("/ws")
async def websocket(websocket: WebSocket):
  await websocket.accept()
  await websocket.send_json({"msg": "Hello WebSocket"})
  await websocket.close()
