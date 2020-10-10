## Copyright (c) 2020 mangalbhaskar.
"""FastAPI sub api

https://fastapi.tiangolo.com/advanced/sub-applications/
https://fastapi.tiangolo.com/advanced/behind-a-proxy/

When you mount a sub-application as described above, FastAPI will take care of communicating the mount path for the sub-application using a mechanism from the ASGI specification called a root_path.

You will learn more about the root_path and how to use it explicitly in the section about Behind a Proxy.

Disable automatic server from root_path
If you don't want FastAPI to include an automatic server using the root_path, you can use the parameter root_path_in_servers=False:
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


from fastapi import FastAPI, Request


app = FastAPI()
# uvicorn main:app --root-path /api/v1
# app = FastAPI(root_path="/api/v1")

# app = FastAPI(
#   servers=[
#     {"url": "https://stag.example.com", "description": "Staging environment"},
#     {"url": "https://prod.example.com", "description": "Production environment"},
#   ],
#   root_path="/api/v1",
#    root_path_in_servers=False,
# )


@app.get("/app")
def read_main():
  return {"message": "Hello World from main app"}


@app.get("/root")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}



subapi = FastAPI()


@subapi.get("/sub")
def read_sub():
  return {"message": "Hello World from sub API"}


app.mount("/subapi", subapi)
