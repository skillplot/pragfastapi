"""Compatibility hook for DBSession for Python 3.6 and 3.7"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'

import platform

from . import database


if float('.'.join(platform.python_version_tuple()[:-1])) == 3.6:
  from fastapi import Request, Response

  @app.middleware("http")
  async def db_session_middleware(request: Request, call_next):
    """Alternative DB session with middleware
    If you can't use dependencies with yield -- for example, if you are not using Python 3.7 and can't install the "backports" mentioned above for Python 3.6 -- you can set up the session in a "middleware" in a similar way.

    A "middleware" is basically a function that is always executed for each request, with some code executed before, and some code executed after the endpoint function."""
    response = Response("Internal server error", status_code=500)
    try:
      request.state.db = database.DBSession()
      response = await call_next(request)
    finally:
      request.state.db.close()
    return response


  # Dependency
  def get_db(request: Request):
    return request.state.db
else:
  ## Dependency
  def get_db():
    db = database.DBSession()
    try:
      yield db
    finally:
      db.close()
