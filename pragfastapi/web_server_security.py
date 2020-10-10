## Copyright (c) 2020 mangalbhaskar.
"""FastAPI Security

https://fastapi.tiangolo.com/tutorial/security/first-steps/
https://fastapi.tiangolo.com/advanced/behind-a-proxy
https://fastapi.tiangolo.com/tutorial/security/get-current-user/

https://en.wikipedia.org/wiki/Security_through_obscurity
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer


app = FastAPI()

## When we create an instance of the OAuth2PasswordBearer class we pass in the tokenUrl parameter. This parameter contains the URL that the client (the frontend running in the user's browser) will use to send the username and password in order to get a token.

## here tokenUrl="token" refers to a relative URL token that we haven't created yet. As it's a relative URL, it's equivalent to ./token. Because we are using a relative URL, if your API was located at https://example.com/, then it would refer to https://example.com/token. But if your API was located at https://example.com/api/v1/, then it would refer to https://example.com/api/v1/token.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

## It will go and look in the request for that Authorization header, check if the value is Bearer plus some token, and will return the token as a str.
## If it doesn't see an Authorization header, or the value doesn't have a Bearer token, it will respond with a 401 status code error (UNAUTHORIZED) directly.
@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
  return {"token": token}
