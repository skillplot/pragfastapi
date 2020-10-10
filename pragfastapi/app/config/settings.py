## Copyright (c) 2020 mangalbhaskar.
"""APP configuration"""
__author__ = 'mangalbhaskar'

from functools import lru_cache
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator
from typing import Any, Dict, List, Optional, Union

from . import (
  apicfg
  ,rediscfg
  ,mongodbcfg
)


class Settings(BaseSettings):
  PROJECT_NAME: str = 'pragmatic-fastapi'
  VERSION: str = '0.1.0'
  DESCRIPTION: str = '''Codebase for Pragmatic FastAPI book from pragmatic python book series. An opinionated fastapi practical tutorials.'''

  SMTP_TLS: bool = True
  SMTP_PORT: Optional[int] = None
  SMTP_HOST: Optional[str] = None
  SMTP_USER: Optional[str] = None
  SMTP_PASSWORD: Optional[str] = None
  EMAILS_FROM_EMAIL: Optional[EmailStr] = None
  EMAILS_FROM_NAME: Optional[str] = None

  @validator("EMAILS_FROM_NAME")
  def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
      if not v:
        return values["PROJECT_NAME"]
      return v

  EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
  EMAIL_TEMPLATES_DIR: str = "/app/templates/build"
  EMAILS_ENABLED: bool = False

  @validator("EMAILS_ENABLED", pre=True)
  def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
      return bool(
          values.get("SMTP_HOST")
          and values.get("SMTP_PORT")
          and values.get("EMAILS_FROM_EMAIL")
      )

  EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
  FIRST_SUPERUSER: Optional[EmailStr] = None
  FIRST_SUPERUSER_PASSWORD: Optional[str] = None
  USERS_OPEN_REGISTRATION: bool = False

  class Config:
      case_sensitive = True


@lru_cache()
def get_app_settings():
  return Settings(), apicfg.Apicfg(), rediscfg.RedisCfg(), mongodbcfg.MongodbCfg()


"""Initialize the core application."""
APPCFG, APICFG, REDISCFG, MONGODBCFG = get_app_settings()
