from pydantic import BaseModel, EmailStr
# from typing import Optional
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    user = "user"

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Role = Role.user

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
