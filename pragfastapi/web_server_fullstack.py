## Copyright (c) 2020 mangalbhaskar.
"""FastAPI based main application server."""
__author__ = 'mangalbhaskar'


import datetime
import os
import sys
import time

import fastapi
from fastapi import staticfiles
from fastapi import templating

from starlette.middleware.cors import CORSMiddleware

from . config import settings
from . utils import web_utils
from . import router


# print("type(appcfg), appcfg: {}, {}".format(type(appcfg), appcfg))
app = fastapi.FastAPI(
  title=settings.APPCFG.PROJECT_NAME
  ,openapi_url=f"{settings.APICFG.API_BASE_URL}/openapi.json"
  ,description=settings.APPCFG.DESCRIPTION
  ,version=settings.APPCFG.VERSION
)

## Set all CORS enabled origins
app.add_middleware(
  CORSMiddleware
  ##,allow_origins=[str(origin) for origin in settings.APPCFG.BACKEND_CORS_ORIGINS]
  ,allow_origins=["*"]
  ,allow_credentials=True
  ,allow_methods=["*"]
  ,allow_headers=["*"]
)

# ## optional, required if you are serving static files
# app.mount("/static", staticfiles.StaticFiles(directory="static"), name="static")

# ## optional, required if you are serving webpage via template engine
# templates = templating.Jinja2Templates(directory="templates")

api_router = router.add_app_routes(settings.APICFG)

app.include_router(
  api_router
  # ,prefix=settings.APICFG.API_BASE_URL
)
