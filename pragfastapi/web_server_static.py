## Copyright (c) 2020 mangalbhaskar.
"""FastAPI static files.

https://fastapi.tiangolo.com/tutorial/static-files/
https://www.starlette.io/staticfiles/

https://fastapi.tiangolo.com/tutorial/static-files/#use-staticfiles
https://github.com/tiangolo/fastapi/issues/130

pip install aiofiles

"Mounting" means adding a complete "independent" application in a specific path, that then takes care of handling all the sub-paths.

This is different from using an APIRouter as a mounted application is completely independent. The OpenAPI and docs from your main application won't include anything from the mounted application, etc.

The first "/static" refers to the sub-path this "sub-application" will be "mounted" on. So, any path that starts with "/static" will be handled by it.

The directory="static" refers to the name of the directory that contains your static files.

The name="static" gives it a name that can be used internally by FastAPI.
"""
__author__ = 'mangalbhaskar'


import fastapi
from fastapi import responses
# from fastapi import staticfiles
from starlette import staticfiles

import pkg_resources


app = fastapi.FastAPI()
app.mount("/web", staticfiles.StaticFiles(directory=pkg_resources.resource_filename(__name__, 'app/_site')), name="web")
app.mount("/site", staticfiles.StaticFiles(directory=pkg_resources.resource_filename(__name__, 'app/_site'), html = True), name="site")


@app.get('/')
def main():
  return {'message':'Static Files serving using FastAPI'}


@app.get("/.*", include_in_schema=False)
def root():
  return responses.HTMLResponse(pkg_resources.resource_string(__name__, 'app/_site/*'))
