## Copyright (c) 2020 mangalbhaskar.
"""FastAPI basic auth

https://fastapi.tiangolo.com/advanced/security/http-basic-auth/

Timing Attacks
But by using the secrets.compare_digest() it will be secure against a type of attacks called "timing attacks".
But what's a "timing attack"?
The time to answer helps the attackers

A "professional" attack
Of course, the attackers would not try all this by hand, they would write a program to do it, possibly with thousands or millions of tests per second. And would get just one extra correct letter at a time.
But doing that, in some minutes or hours the attackers would have guessed the correct username and password, with the "help" of our application, just using the time taken to answer.

Fix it with secrets.compare_digest()
But in our code we are actually using secrets.compare_digest().

In short, it will take the same time to compare stanleyjobsox to stanleyjobson than it takes to compare johndoe to stanleyjobson. And the same for the password.
That way, using secrets.compare_digest() in your application code, it will be safe against this whole range of security attacks.

https://fastapi.tiangolo.com/advanced/using-request-directly/
https://www.starlette.io/requests/
By declaring a path operation function parameter with the type being the Request FastAPI will know to pass the Request in that parameter.
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


import secrets

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


app = FastAPI()

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
  correct_username = secrets.compare_digest(credentials.username, "stanleyjobson")
  correct_password = secrets.compare_digest(credentials.password, "swordfish")
  if not (correct_username and correct_password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect email or password",
      headers={"WWW-Authenticate": "Basic"},
    )
  return credentials.username


@app.get("/")
def main(username: str = Depends(get_current_username)):
  return {"username": username}


@app.get("/items/{item_id}")
def read_root(item_id: str, request: Request):
  client_host = request.client.host
  return {"client_host": client_host, "item_id": item_id}


@app.get("/items/{item_id}")
def read_root(item_id: str, request: Request):
  client_host = request.client.host
  return {"client_host": client_host, "item_id": item_id}
