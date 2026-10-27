from pydantic import BaseModel, EmailStr

class Account(BaseModel):
    username: str
    password: str
    role: str
    email: EmailStr

class AccountResponse(BaseModel):
    username: str
    role: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str
