from pydantic import BaseModel
from enum import Enum


class RoleEnum(str, Enum):
    guest = "guest"
    client = "client"
    admin = "admin"


class UserCreate(BaseModel):
    username: str
    password: str
    role: RoleEnum = RoleEnum.guest


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
