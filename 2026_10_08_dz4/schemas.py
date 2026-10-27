from pydantic import BaseModel, EmailStr

class UserProfileBase(BaseModel):
    username: str
    email: EmailStr
    age: int

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(UserProfileBase):
    pass

class UserProfileResponse(UserProfileBase):
    id: int

    class Config:
        from_attributes = True
