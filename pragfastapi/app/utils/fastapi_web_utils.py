## Copyright (c) 2020 mangalbhaskar.
"""fastapi common utility functions.

https://fastapi.tiangolo.com/advanced/websockets/
"""
__author__ = 'mangalbhaskar'


from typing import Optional
from fastapi import Cookie, Query, WebSocket, status


async def get_cookie_or_token(
  websocket: WebSocket,
  session: Optional[str] = Cookie(None),
  token: Optional[str] = Query(None),
):
  if session is None and token is None:
    await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
  return session or token
