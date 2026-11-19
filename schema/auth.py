from pydantic import BaseModel,EmailStr,Field,ConfigDict
from typing import Optional
class CreateUser(BaseModel):
    username:str=Field(min_length=3,max_length=50)
    email:EmailStr=Field(min_length=5,max_length=50)
    password:str=Field(min_length=8,max_length=200)
class ResponseUser(BaseModel):
    id:int=Field(ge=1,le=100)
    username:str=Field(min_length=3,max_length=50)
    email:EmailStr=Field(min_length=5,max_length=50)
    password:str=Field(min_length=8,max_length=200)
    is_active:bool
    role:str=Field(min_length=3,max_length=50)
    model_config=ConfigDict(from_attributes=True)
class UpdateUser(BaseModel):
    username:str|None=Field(default=None,min_length=3,max_length=50)
    email:EmailStr|None=Field(default=None,min_length=5,max_length=50)
    password:str|None=Field(default=None,min_length=8,max_length=200)
class LoginUser(BaseModel):
    email:EmailStr=Field(min_length=5,max_length=50)
    password:str=Field(min_length=8,max_length=200)
class TokenResponse(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str
class RefreshTokenRequest(BaseModel):
    refresh_token:str