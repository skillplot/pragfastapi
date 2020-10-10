## Copyright (c) 2020 mangalbhaskar.
"""Mongodb configurations"""
__author__ = 'mangalbhaskar'

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings, validator, AnyHttpUrl, PostgresDsn


##-------------------------------
## Mongodb configuration
##-------------------------------
class MongodbCfg(BaseSettings):
  HOST: str = 'localhost'
  PORT: int = 27017
  DB: Optional[str] = None
  USER: Optional[str] = None
  PASSWORD: Optional[str] = None
  ##
  SERVER_NAME: str = 'localhost'
  SERVER_HOST: Optional[AnyHttpUrl]
  DATABASE_URI: Optional[PostgresDsn] = None


  # @validator("DATABASE_URI", pre=True)
  # def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
  #   if isinstance(v, str):
  #     return v
  #   return PostgresDsn.build(
  #     scheme="mongodb"
  #     ,host=values.get("SERVER")
  #     # ,user=values.get("USER")
  #     # ,password=values.get("PASSWORD")
  #     ,path=f"/{values.get('DB') or ''}"
  #   )


  class Config:
      case_sensitive = True
