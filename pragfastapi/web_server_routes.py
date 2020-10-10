## Copyright (c) 2020 mangalbhaskar.
"""FastAPI routing for bigger applications.

https://fastapi.tiangolo.com/tutorial/bigger-applications/
https://docs.python.org/3/tutorial/modules.html

You don't have to worry about performance when including routers.
This will take microseconds and will only happen at startup.
So it won't affect performance.
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


from fastapi import Depends, FastAPI, Header, HTTPException

from .app.routes import items, users


app = FastAPI()


async def get_token_header(x_token: str = Header(...)):
  if x_token != "fake-super-secret-token":
    raise HTTPException(status_code=400, detail="X-Token header invalid")


## With app.include_router() we can add an APIRouter to the main FastAPI application.
app.include_router(users.router)
app.include_router(
  items.router,
  prefix="/items",
  tags=["items"],
  dependencies=[Depends(get_token_header)],
  responses={404: {"description": "Not found"}},
)


