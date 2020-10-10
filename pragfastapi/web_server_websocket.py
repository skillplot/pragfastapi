## Copyright (c) 2020 mangalbhaskar.
"""FastAPI based main application server.

WebSocket API
https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API
The WebSocket API is an advanced technology that makes it possible to open a two-way interactive communication session between the user's browser and a server. With this API, you can send messages to a server and receive event-driven responses without having to poll the server for a reply.

WebSocket_servers
https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers
A WebSocket server is nothing more than an application listening on any port of a TCP server that follows a specific protocol. 

https://en.wikipedia.org/wiki/Reverse_proxy
http://www.steves-internet-guide.com/tcpip-ports-sockets/
http://www.steves-internet-guide.com/internet-protocol-suite-explained/
https://www.ibm.com/support/knowledgecenter/en/SSB27H_6.2.0/fa2ti_what_is_socket_connection.html
https://en.wikipedia.org/wiki/Network_socket
https://fastapi.tiangolo.com/advanced/websockets/

https://www.starlette.io/websockets/
https://www.starlette.io/endpoints/#websocketendpoint
"""
__author__ = 'mangalbhaskar'


import fastapi
from fastapi import Depends
# from fastapi import responses
from starlette import responses

# from fastapi import WebSocket
from starlette.websockets import WebSocket, WebSocketDisconnect
from starlette import staticfiles

from typing import Optional
import pkg_resources

from app.utils import fastapi_web_utils

app = fastapi.FastAPI()
app.mount('/web', staticfiles.StaticFiles(directory=pkg_resources.resource_filename(__name__, 'app/_site')), name='web')
app.mount('/site', staticfiles.StaticFiles(directory=pkg_resources.resource_filename(__name__, 'app/_site'), html = True), name='site')


@app.get('/')
def main():
  return {'message':'Web socket server using FastAPI'}


@app.get('/chat')
def chat():
  htmlfile = pkg_resources.resource_string(__name__, 'app/_site/websocket-1.html')
  return responses.HTMLResponse(htmlfile)


@app.get('/chat/{chati}')
def chati(chati: int):
  htmlfile = pkg_resources.resource_string(__name__, 'app/_site/websocket-{}.html'.format(str(chati)))
  return responses.HTMLResponse(htmlfile)


@app.get('/.*', include_in_schema=False)
def _root():
  return responses.HTMLResponse(pkg_resources.resource_string(__name__, 'app/_site/*'))


@app.websocket('/ws')
async def ws(websocket: WebSocket):
  await websocket.accept()
  while True:
    data = await websocket.receive_text()
    await websocket.send_text(f'Message text was: {data}')

from app.entities import WsConnectionManager
connection_manager = WsConnectionManager.ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
  await connection_manager.connect(websocket)
  try:
    while True:
      data = await websocket.receive_text()
      await connection_manager.send_personal_message(f"You wrote: {data}", websocket)
      await connection_manager.broadcast(f"Client #{client_id} says: {data}")
  except WebSocketDisconnect:
    connection_manager.disconnect(websocket)
    await connection_manager.broadcast(f"Client #{client_id} left the chat")


@app.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
  websocket: WebSocket,
  item_id: str,
  q: Optional[int] = None,
  cookie_or_token: str = Depends(fastapi_web_utils.get_cookie_or_token),
):
  """The app above is a minimal and simple example to demonstrate how to handle and broadcast messages to several WebSocket connections.
  But have in mind that, as everything is handled in memory, in a single list, it will only work while the process is running, and will only work with a single process.

  https://fastapi.tiangolo.com/advanced/websockets/
  https://github.com/encode/broadcaster
  """
  await websocket.accept()
  while True:
    data = await websocket.receive_text()
    await websocket.send_text(
      f"Session cookie or query token value is: {cookie_or_token}"
    )
    if q is not None:
      await websocket.send_text(f"Query parameter q is: {q}")
    await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")
