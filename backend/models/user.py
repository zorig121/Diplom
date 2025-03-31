from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    fullname: str

class LoginRequest(BaseModel):
    username: str
    password: str
