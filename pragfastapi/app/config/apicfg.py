## Copyright (c) 2020 mangalbhaskar.
"""API configuration"""
__author__ = 'mangalbhaskar'

import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings, validator, AnyHttpUrl


##-------------------------------
## API Base URL configuration
##-------------------------------
class Apicfg(BaseSettings):
  API_BASE_VERSION: str = 'v3'
  API_BASE_URL: str = '/api/v3'
  WEB_APP_NAME: str = 'pragmatic-fastapi'
  SECRET_KEY: str = secrets.token_urlsafe(32)
  ## 60 minutes * 24 hours * 8 days = 8 days
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
  HOST: str = 'localhost'
  SERVER_NAME: str = 'localhost'
  SERVER_HOST: Optional[AnyHttpUrl]
  # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
  # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
  # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
  BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []


  @validator("BACKEND_CORS_ORIGINS", pre=True)
  def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
      if isinstance(v, str) and not v.startswith("["):
          return [i.strip() for i in v.split(",")]
      elif isinstance(v, (list, str)):
          return v
      raise ValueError(v)

  LOG_TIMESTAMP: bool = False
  ALLOWED_FILE_TYPE: List[str] = [
    '.txt'
    ,'.csv'
    ,'.yml'
    ,'.json'
  ]
  ALLOWED_IMAGE_TYPE: List[str] = [
    '.pdf'
    ,'.png'
    ,'.jpg'
    ,'.jpeg'
    ,'.tiff'
    ,'.gif'
  ]
  ALLOWED_VIDEO_TYPE: List[str] = ['.mp4']
  FILE_DELIMITER: str = ';'


  class Config:
      case_sensitive = True
