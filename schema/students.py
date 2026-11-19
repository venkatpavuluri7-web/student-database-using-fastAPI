from typing import Optional

from pydantic import BaseModel,Field,EmailStr,ConfigDict
class createStudent(BaseModel):
    name:str=Field(min_length=2,max_length=20)
    age:int=Field(ge=6,le=23)
    email:EmailStr=Field(min_length=5,max_length=25)
    phoneNumber:str|None=Field(default=None,min_length=10,max_length=15)

class ResponseStudent(BaseModel):
    id:int=Field(ge=1,le=100)
    name:str=Field(min_length=2,max_length=20)
    age:int=Field(ge=6,le=23)
    email:EmailStr=Field(min_length=5,max_length=25)
    phoneNumber:Optional[str]=None
    model_config=ConfigDict(from_attributes=True)
class UpdateStudent(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    age: int | None = Field(
        default=None,
        ge=1,
        le=100
    )

    email: EmailStr | None = None
    phoneNumber:str |None=Field(default=None,min_length=10,max_length=15) 
    
    