from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


# Foydalanuvchini qaytarish uchun — hashed_password bu yerda YO'Q
class UserOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
