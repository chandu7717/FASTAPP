from typing import List

from pydantic import BaseModel, EmailStr


class BlogBase(BaseModel):
    title: str
    body: str
    # user_id: int


class Blog(BlogBase):
    class Config():
        from_attributes = True


class Users(BaseModel):
    name: str
    email: EmailStr
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog]

    class Config():
        from_attributes = True


class ShowBlog(BaseModel):
    title: str
    body: str
    id: int
    creator: ShowUser

    class Config():
        from_attributes = True


class User_login(BaseModel):
    username: EmailStr
    password: str


# For the access token JWT
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):        #to return the token data  c TokenData(email="alice@example.com") and then assigning with the decodeded token username
    userID: str | None = None

class RefreshTokenRequest(BaseModel):    #To accept the token from the request
    refresh_token:str
