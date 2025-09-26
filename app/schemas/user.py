from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator

class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr 
    phone_number: Optional[str]
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

    @field_validator("phone_number")
    def empty_string_to_none(cls, value):
        if value is not None and value.strip() == "":
            return None
        return value

class UserRead(BaseModel):

    username: str
    email: str
    phone_number: Optional[str] = None
    profile_image_url: Optional[str] = None
    bio: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    identifier: str
    password: str

class UserLoginSuccess(BaseModel):
    user: UserRead
    message: str
    access_token: str
    token_type: str