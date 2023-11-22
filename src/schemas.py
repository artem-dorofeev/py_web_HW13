from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr



class ContactModel(BaseModel): 

    firstname: str = Field(min_length=2, max_length=20)
    lastname: str = Field(min_length=2, max_length=20)
    email: str = EmailStr 
    phone: str = Field(min_length=2, max_length=20)
    birthday: date
    additional: str = Field()



class ContactResponse(BaseModel):
    id: int = 1
    firstname: str
    lastname: str
    email: str = EmailStr
    phone: str
    birthday: date
    additional: str 
    created_at: datetime
    updated_at: datetime

    class Config:
        #orm_mode = True
        from_attributes = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        # orm_mode = True
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"