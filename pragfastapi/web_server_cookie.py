## Copyright (c) 2020 mangalbhaskar.
"""FastAPI cookie.

https://fastapi.tiangolo.com/advanced/response-cookies/
https://www.starlette.io/responses/#set-cookie

https://fastapi.tiangolo.com/advanced/response-headers/

https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers
https://www.starlette.io/middleware/#corsmiddleware
custom proprietary headers can be added using the 'X-' prefix.

But if you have custom headers that you want a client in a browser to be able to see, you need to add them to your CORS configurations (read more in CORS (Cross-Origin Resource Sharing)), using the parameter expose_headers documented in Starlette's CORS docs

https://fastapi.tiangolo.com/advanced/response-change-status-code/
For example, imagine that you want to return an HTTP status code of "OK" 200 by default.
But if the data didn't exist, you want to create it, and return an HTTP status code of "CREATED" 201.
But you still want to be able to filter and convert the data you return with a response_model.
For those cases, you can use a Response parameter.
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'

from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse


tasks = {"foo": "Listen to the Bar Fighters"}

app = FastAPI()


@app.post("/cookie/")
def create_cookie():
  content = {"message": "Come to the dark side, we have cookies"}
  response = JSONResponse(content=content)
  response.set_cookie(key="fakesession", value="fake-cookie-session-value")
  return response


@app.get("/headers-and-object/")
def get_headers_and_object(response: Response):
  response.headers["X-Cat-Dog"] = "alone in the world"
  return {"message": "Hello World"}


@app.get("/headers/")
def get_headers():
  content = {"message": "Hello World"}
  headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
  return JSONResponse(content=content, headers=headers)



@app.put("/get-or-create-task/{task_id}", status_code=200)
def get_or_create_task(task_id: str, response: Response):
  if task_id not in tasks:
    tasks[task_id] = "This didn't exist before"
    response.status_code = status.HTTP_201_CREATED
  return tasks[task_id]
