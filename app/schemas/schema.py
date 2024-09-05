from pydantic import BaseModel, EmailStr
from typing import List


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class BlogCreate(BaseModel):
    title: str
    content: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    blogs: List[BlogCreate] = []

    class Config:
        from_attributes = True


class BlogRead(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    owner: UserRead

    class Config:
        from_attributes = True

class Login(BaseModel):
    email: EmailStr
    password: str

class GetToken(BaseModel):
    access_token: str