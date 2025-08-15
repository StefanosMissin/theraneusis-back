from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str
    tenant_id: str


class LoginPayload(BaseModel):
    email: EmailStr
    password: str

class RegisterPayload(BaseModel):
    first_name: str
    last_name: str
    full_name: str
    email: EmailStr
    password: str
    confirm_password: str
    role: str
    turnstile_token: str

class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetPayload(BaseModel):
    token: str
    password: str
