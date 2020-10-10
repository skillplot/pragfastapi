## Copyright (c) 2020 mangalbhaskar.
"""FastAPI based main application server."""
__author__ = 'mangalbhaskar'


import fastapi

from starlette.middleware.cors import CORSMiddleware

from . config import settings

app = fastapi.FastAPI(
  title=settings.APPCFG.PROJECT_NAME
  ,openapi_url=f"{settings.APICFG.API_BASE_URL}/openapi.json"
  ,description=settings.APPCFG.DESCRIPTION
  ,version=settings.APPCFG.VERSION
)

## Set all CORS enabled origins
app.add_middleware(
  CORSMiddleware
  ,allow_origins=["*"]
  ,allow_credentials=True
  ,allow_methods=["*"]
  ,allow_headers=["*"]
)

@app.get('/')
def main():
  return {'settings': settings}
