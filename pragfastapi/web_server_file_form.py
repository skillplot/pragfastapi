## Copyright (c) 2020 mangalbhaskar.
"""FastAPI request file

https://fastapi.tiangolo.com/tutorial/request-files/
Use File to declare files to be uploaded as input parameters (as form data).


# To declare File bodies, you need to use File, because otherwise the parameters would be interpreted as query parameters or body (JSON) parameters.

https://andrew-d.github.io/python-multipart/
https://docs.python.org/3/glossary.html#term-file-like-object
https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile

When you use the async methods, FastAPI runs the file methods in a threadpool and awaits for them.

FastAPI's UploadFile inherits directly from Starlette's UploadFile, but adds some necessary parts to make it compatible with Pydantic and the other parts of FastAPI.

The way HTML forms (<form></form>) sends the data to the server normally uses a "special" encoding for that data, it's different from JSON.

Data from forms is normally encoded using the "media type" application/x-www-form-urlencoded when it doesn't include files.

But when the form includes files, it is encoded as multipart/form-data. If you use File, FastAPI will know it has to get the files from the correct part of the body.

You can declare multiple File and Form parameters in a path operation, but you can't also declare Body fields that you expect to receive as JSON, as the request will have the body encoded using multipart/form-data instead of application/json.

This is not a limitation of FastAPI, it's part of the HTTP protocol.

https://fastapi.tiangolo.com/tutorial/request-forms-and-files/
You can define files and form fields at the same time using File and Form.
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


from typing import List

import fastapi
from fastapi import File, Form, UploadFile
# from fastapi import responses
from starlette import responses

from starlette import staticfiles

import pkg_resources


app = fastapi.FastAPI()
app.mount('/web', staticfiles.StaticFiles(directory=pkg_resources.resource_filename(__name__, 'app/_site')), name='web')
app.mount('/site', staticfiles.StaticFiles(directory=pkg_resources.resource_filename(__name__, 'app/_site'), html = True), name='site')


@app.get('/')
def main():
  htmlfile = pkg_resources.resource_string(__name__, 'app/_site/upload.html')
  return responses.HTMLResponse(htmlfile)


@app.post("/files/")
async def create_file(
    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }

