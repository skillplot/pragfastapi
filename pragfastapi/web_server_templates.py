## Copyright (c) 2020 mangalbhaskar.
"""FastAPI templates.

https://fastapi.tiangolo.com/advanced/templates/
https://www.starlette.io/templates/

You could also use from starlette.templating import Jinja2Templates.

Notice that you have to pass the request as part of the key-value pairs in the context for Jinja2. So, you also have to declare it in your path operation.
By declaring response_class=HTMLResponse the docs UI will be able to know that the response will be HTML.
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


import fastapi
from fastapi import responses
## from fastapi import staticfiles
from starlette import staticfiles
from fastapi import templating

from starlette.middleware.cors import CORSMiddleware

import pkg_resources

app = fastapi.FastAPI()
# app.mount("/web", staticfiles.StaticFiles(directory=pkg_resources.resource_filename(__name__, 'app/_site')), name="web")
# app.mount("/site", staticfiles.StaticFiles(directory=pkg_resources.resource_filename(__name__, 'app/_site'), html = True), name="site")

## optional, required if you are serving webpage via template engine
templates = templating.Jinja2Templates(directory=pkg_resources.resource_filename(__name__, 'app/templates'), html = True)



# @app.get('/')
# def main():
#   return {'message':'Static Files serving using FastAPI'}


# @app.get("/.*", include_in_schema=False)
# def root():
#   return responses.HTMLResponse(pkg_resources.resource_string(__name__, 'app/_site/*'))


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
  return templates.TemplateResponse("item.html", {"request": request, "id": id})
