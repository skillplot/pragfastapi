## Copyright (c) 2020 mangalbhaskar.
"""Redis configurations"""
__author__ = 'mangalbhaskar'

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings, validator, AnyHttpUrl, RedisDsn


##-------------------------------
## Redis configuration
##-------------------------------
class RedisCfg(BaseSettings):
  HOST: str = 'localhost'
  PORT: int = 6379
  DB: int = 0
  PASSWORD: Optional[str] = None
  SOCKET_TIMEOUT: Optional[int] = None
  SOCKET_CONNECT_TIMEOUT: Optional[int] = None
  SOCKET_KEEPALIVE: Optional[str] = None
  SOCKET_KEEPALIVE_OPTIONS: Optional[str] = None
  CONNECTION_POOL: Optional[str] = None
  UNIX_SOCKET_PATH: Optional[str] = None
  ENCODING: str = 'utf-8'
  ENCODING_ERRORS: str = 'strict'
  CHARSET: Optional[str] = None
  ERRORS: Optional[str] = None
  DECODE_RESPONSES: bool = False
  RETRY_ON_TIMEOUT: bool = False
  SSL: bool = False
  SSL_KEYFILE: Optional[str] = None
  SSL_CERTFILE: Optional[str] = None
  SSL_CERT_REQS: str = 'required'
  SSL_CA_CERTS: Optional[str] = None
  MAX_CONNECTIONS: Optional[str] = None
  SINGLE_CONNECTION_CLIENT: bool = False
  HEALTH_CHECK_INTERVAL: str = 0

  ##
  SERVER_NAME: str = 'localhost'
  SERVER_HOST: Optional[AnyHttpUrl]
  # USER: str
  IMAGE_QUEUE: str = 'image_queue'
  BATCH_SIZE: int = 1
  SERVER_SLEEP: float = 0.25
  CLIENT_SLEEP: float = 0.25
  IMAGE_DTYPE: str = 'float32'
  CLIENT_MAX_TRIES: int = 100
  DATABASE_URI: Optional[RedisDsn] = None


  # @validator('DATABASE_URI', pre=True)
  # def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
  #   if isinstance(v, str):
  #     return v
  #   return RedisDsn.build(
  #     host=values.get('HOST')
  #     ,port=values.get('PORT')
  #     ,db=values.get('DB')
  #     ##
  #     # ,password=values.get('password')
  #     # ,socket_timeout=values.get('socket_timeout')
  #     # ,socket_connect_timeout=values.get('socket_connect_timeout')
  #     # ,socket_keepalive=values.get('socket_keepalive')
  #     # ,socket_keepalive_options=values.get('socket_keepalive_options')
  #     # ,connection_pool=values.get('connection_pool')
  #     # ,unix_socket_path=values.get('unix_socket_path')
  #     # ,encoding=values.get('encoding')
  #     # ,encoding_errors=values.get('encoding_errors')
  #     # ,charset=values.get('charset')
  #     # ,errors=values.get('errors')
  #     # ,decode_responses=values.get('decode_responses')
  #     # ,retry_on_timeout=values.get('retry_on_timeout')
  #     # ,ssl=values.get('ssl')
  #     # ,ssl_keyfile=values.get('ssl_keyfile')
  #     # ,ssl_certfile=values.get('ssl_certfile')
  #     # ,ssl_cert_reqs=values.get('ssl_cert_reqs')
  #     # ,ssl_ca_certs=values.get('ssl_ca_certs')
  #     # ,max_connections=values.get('max_connections')
  #     # ,single_connection_client=values.get('single_connection_client')
  #     # ,health_check_interval=values.get('health_check_interval')
  #   )


  class Config:
      case_sensitive = True
