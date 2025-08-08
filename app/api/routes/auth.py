from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.core.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.schemas.auth import Token, LoginPayload
from app.services.auth_service import register_user, authenticate_user, login_user
from app.core.security import create_email_verification_token
from app.services.email_service import send_verification_email
from app.core.config import settings
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    tenant_id = "default-tenant"  # Replace with real tenant logic
    user = register_user(db, user_in, tenant_id)
    # Create verification token and send email
    token = create_email_verification_token(user.id)
    send_verification_email(user.email, token)

    return user


@router.post("/login", response_model=Token)
def login(payload: LoginPayload, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return login_user(user)


@router.get("/verify-email")
def verify_email(token: str, email: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Match both user_id and email
    user = db.query(User).filter(User.id == user_id, User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_verified:
        user.is_verified = True
        db.commit()

    return {"message": "Email verified successfully"}

