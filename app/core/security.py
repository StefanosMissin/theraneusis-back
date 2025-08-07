from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_token(data: dict, expires_delta: timedelta, secret: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm=settings.JWT_ALGORITHM)

def create_access_token(user_id: str, tenant_id: str):
    return create_token(
        {"sub": user_id, "tenant_id": tenant_id},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        settings.JWT_SECRET
    )

def create_refresh_token(user_id: str, tenant_id: str):
    return create_token(
        {"sub": user_id, "tenant_id": tenant_id},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        settings.JWT_SECRET
    )

def create_email_verification_token(user_id: str):
    expire = datetime.utcnow() + timedelta(hours=24)
    data = {"sub": user_id, "exp": expire}
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)