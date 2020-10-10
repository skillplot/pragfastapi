## Copyright (c) 2020 mangalbhaskar.
"""FastAPI Security

https://fastapi.tiangolo.com/tutorial/security/first-steps/
https://fastapi.tiangolo.com/advanced/behind-a-proxy
https://fastapi.tiangolo.com/tutorial/security/get-current-user/
https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'

from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


fake_users_db = {
  "johndoe": {
    "username": "johndoe",
    "full_name": "John Doe",
    "email": "johndoe@example.com",
    "hashed_password": "fakehashedsecret",
    "disabled": False,
  },
  "alice": {
    "username": "alice",
    "full_name": "Alice Wonderson",
    "email": "alice@example.com",
    "hashed_password": "fakehashedsecret2",
    "disabled": True,
  },
}

app = FastAPI()


def fake_hash_password(password: str):
  return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
  username: str
  email: Optional[str] = None
  full_name: Optional[str] = None
  disabled: Optional[bool] = None


class UserInDB(User):
  hashed_password: str


def get_user(db, username: str):
  if username in db:
    user_dict = db[username]
    return UserInDB(**user_dict)


def fake_decode_token(token):
  # This doesn't provide any security at all
  # Check the next version
  user = get_user(fake_users_db, token)
  return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
  """
  The additional header WWW-Authenticate with value Bearer we are returning here is also part of the spec.

  Any HTTP (error) status code 401 "UNAUTHORIZED" is supposed to also return a WWW-Authenticate header.

  In the case of bearer tokens (our case), the value of that header should be Bearer.

  You can actually skip that extra header and it would still work.

  But it's provided here to be compliant with the specifications.

  Also, there might be tools that expect and use it (now or in the future) and that might be useful for you or your users, now or in the future.
  """
  user = fake_decode_token(token)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid authentication credentials",
      headers={"WWW-Authenticate": "Bearer"},
    )
  return user


## Only get a user if the user exists, was correctly authenticated, and is active
async def get_current_active_user(current_user: User = Depends(get_current_user)):
  if current_user.disabled:
    raise HTTPException(status_code=400, detail="Inactive user")
  return current_user



@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
  """
  OAuth2PasswordRequestForm is a class dependency that declares a form body with:

  The username
  The password
  ##An optional scope field as a big string, composed of strings separated by spaces.
  An optional grant_type
  An optional client_id
  An optional client_secret

  The OAuth2 spec actually requires a field grant_type with a fixed value of password, but OAuth2PasswordRequestForm doesn't enforce it.

  If you need to enforce it, use OAuth2PasswordRequestFormStrict instead of OAuth2PasswordRequestForm.

  You should never save plaintext passwords, so, we'll use the (fake) password hashing system.


  The response of the token endpoint must be a JSON object.
  It should have a token_type. In our case, as we are using "Bearer" tokens, the token type should be "bearer".

  And it should have an access_token, with a string containing our access token.

  For this simple example, we are going to just be completely insecure and return the same username as the token.

  By the spec, you should return a JSON with an access_token and a token_type, the same as in this example.
  This is something that you have to do yourself in your code, and make sure you use those JSON keys.
  It's almost the only thing that you have to remember to do correctly yourself, to be compliant with the specifications.
  For the rest, FastAPI handles it for you.
  """
  user_dict = fake_users_db.get(form_data.username)
  if not user_dict:
    raise HTTPException(status_code=400, detail="Incorrect username or password")
  user = UserInDB(**user_dict)
  hashed_password = fake_hash_password(form_data.password)
  if not hashed_password == user.hashed_password:
    raise HTTPException(status_code=400, detail="Incorrect username or password")

  return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
  return current_user
