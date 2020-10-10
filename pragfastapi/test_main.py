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

Note that the TestClient receives data that can be converted to JSON, not Pydantic models.

If you have a Pydantic model in your test and you want to send its data to the application during testing, you can use the jsonable_encoder descibed in JSON Compatible Encoder.
https://fastapi.tiangolo.com/tutorial/encoder/

https://fastapi.tiangolo.com/advanced/testing-websockets/
https://fastapi.tiangolo.com/advanced/testing-events/
https://fastapi.tiangolo.com/advanced/testing-dependencies/
https://fastapi.tiangolo.com/advanced/testing-database/


https://fastapi.tiangolo.com/advanced/async-tests/
You have already seen how to test your FastAPI applications using the provided TestClient, but with it, you can't test or run any other async function in your (synchronous) pytest functions.

Being able to use asynchronous functions in your tests could be useful, for example, when you're querying your database asynchronously. Imagine you want to test sending requests to your FastAPI application and then verify that your backend successfully wrote the correct data in the database, while using an async database library.
If we want to call asynchronous functions in our tests, our test functions have to be asynchronous. Pytest provides a neat library for this, called pytest-asyncio, that allows us to specify that some test functions are to be called asynchronously.

pip install pytest-asyncio

By running our tests asynchronously, we can no longer use the TestClient inside our test functions.
Luckily there's a nice alternative, called HTTPX.

HTTPX is an HTTP client for Python 3 that allows us to query our FastAPI application similarly to how we did it with the TestClient.
the Requests library, you'll find that the API of HTTPX is almost identical.
The important difference for us is that with HTTPX we are not limited to synchronous, but can also make asynchronous requests.

https://www.python-httpx.org/
HTTPX is a fully featured HTTP client for Python 3, which provides sync and async APIs, and support for both HTTP/1.1 and HTTP/2.

https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop
https://github.com/pytest-dev/pytest-asyncio/issues/38#issuecomment-264418154
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


from fastapi.testclient import TestClient

from . web_server_testing import app

client = TestClient(app)


def test_read_main():
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {"msg": "Hello World"}


def test_read_item():
  response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
  assert response.status_code == 200
  assert response.json() == {
    "id": "foo",
    "title": "Foo",
    "description": "There goes my hero",
  }


def test_read_item_bad_token():
  response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
  assert response.status_code == 400
  assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_inexistent_item():
  response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
  assert response.status_code == 404
  assert response.json() == {"detail": "Item not found"}


def test_create_item():
  response = client.post(
    "/items/",
    headers={"X-Token": "coneofsilence"},
    json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
  )
  assert response.status_code == 200
  assert response.json() == {
    "id": "foobar",
    "title": "Foo Bar",
    "description": "The Foo Barters",
  }


def test_create_item_bad_token():
  response = client.post(
    "/items/",
    headers={"X-Token": "hailhydra"},
    json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
  )
  assert response.status_code == 400
  assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_existing_item():
  response = client.post(
      "/items/",
      headers={"X-Token": "coneofsilence"},
      json={
        "id": "foo",
        "title": "The Foo ID Stealers",
        "description": "There goes my stealer",
      },
  )
  assert response.status_code == 400
  assert response.json() == {"detail": "Item already exists"}


def test_websocket():
  client = TestClient(app)
  with client.websocket_connect("/ws") as websocket:
    data = websocket.receive_json()
    assert data == {"msg": "Hello WebSocket"}


def test_read_items():
  with TestClient(app) as client:
    response = client.get("/items/foo")
    assert response.status_code == 200
    assert response.json() == {"name": "Fighters"}
