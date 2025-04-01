from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    fullname: str

class LoginRequest(BaseModel):
    username: str
    password: str

class UserInDB(BaseModel):
    username: str
    email: EmailStr
    fullname: str
    hashed_password: str
    is_active: bool = True
    roles: List[str] = ["user"]
    created_at: datetime = datetime.utcnow()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
