## Copyright (c) 2020 mangalbhaskar.
"""FastAPI events.

https://fastapi.tiangolo.com/advanced/events/
https://www.starlette.io/events/

You can define event handlers (functions) that need to be executed before the application starts up, or when the application is shutting down.
These functions can be declared with async def or normal def.

Only event handlers for the main application will be executed, not for Sub Applications - Mounts.

Here, the shutdown event handler function will write a text line "Application shutdown" to a file log.txt.

In the open() function, the mode="a" means "append", so, the line will be added after whatever is on that file, without overwriting the previous contents.

Notice that in this case we are using a standard Python open() function that interacts with a file.

So, it involves I/O (input/output), that requires "waiting" for things to be written to disk.

But open() doesn't use async and await.

So, we declare the event handler function with standard def instead of async def.
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


from fastapi import FastAPI

app = FastAPI()

items = {}


@app.on_event("startup")
async def startup_event():
  items["foo"] = {"name": "Fighters"}
  items["bar"] = {"name": "Tenders"}


@app.on_event("shutdown")
def shutdown_event():
  with open("log.txt", mode="a") as log:
    log.write("Application shutdown")


@app.get("/items/")
async def read_items():
  return [{"name": "Foo"}]


@app.get("/items/{item_id}")
async def read_items(item_id: str):
  return items[item_id]
