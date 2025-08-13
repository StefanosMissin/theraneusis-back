from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    doctor = "doctor"
    client = "client"
    admin = "admin"

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: str
    tenant_id: str

    class Config:
        orm_mode = True

class RegisterPayload(BaseModel):
    first_name: str
    last_name: str
    full_name: str
    email: EmailStr
    password: str
    confirm_password: str
    role: str
    turnstile_token: str