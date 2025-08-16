from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.core.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.schemas.auth import Token, LoginPayload, RegisterPayload, PasswordResetRequest, PasswordResetPayload 
from app.services.auth_service import register_user, authenticate_user, login_user, get_password_hash    
from app.core.security import create_email_verification_token
from app.services.email_service import send_verification_email, send_password_reset_email
from app.core.config import settings
from app.models.user import User
from datetime import datetime, timedelta
import requests

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut)
def register(payload: RegisterPayload, db: Session = Depends(get_db)):
    # Verify Turnstile token
    verify_url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    data = {
        "secret": settings.TURNSTILE_SECRET_KEY.get_secret_value(),
        "response": payload.turnstile_token,
    }
    resp = requests.post(verify_url, data=data)
    result = resp.json()
    if not result.get("success"):
        raise HTTPException(status_code=400, detail="Invalid CAPTCHA")

    # Prepare user input for registration
    user_in = UserCreate(
        first_name=payload.first_name,
        last_name=payload.last_name,
        full_name=payload.full_name,
        email=payload.email,
        password=payload.password,
        role=payload.role,
    )
    tenant_id = "default-tenant"  # Replace with real tenant logic
    user = register_user(db, user_in, tenant_id)
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
            return {"success": False, "error": "Invalid token payload"}

        user = db.query(User).filter(User.id == user_id, User.email == email).first()
        if not user:
            return {"success": False, "error": "User not found"}

        if not user.is_verified:
            user.is_verified = True
            db.commit()

        return {"success": True, "message": "Email verified successfully"}

    except JWTError:
        return {"success": False, "error": "Invalid or expired token"}


@router.post("/logout")
def logout(response: Response):
    response.set_cookie(
        key="access_token",
        value="",
        max_age=0,
        path="/",
        httponly=True,
        secure=True,
        samesite="lax"
    )
    response.set_cookie(
        key="refresh_token",
        value="",
        max_age=0,
        path="/",
        httponly=True,
        secure=True,
        samesite="lax"
    )
    response.set_cookie(
        key="token_type",
        value="",
        max_age=0,
        path="/",
        httponly=True,
        secure=True,
        samesite="lax"
    )
    return {"message": "Logged out successfully"}



@router.post("/request-password-reset")
def request_password_reset(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    # ✅ Turnstile CAPTCHA validation
    verify_url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    data = {
        "secret": settings.TURNSTILE_SECRET_KEY.get_secret_value(),
        "response": payload.turnstile_token,
    }
    resp = requests.post(verify_url, data=data)
    result = resp.json()
    if not result.get("success"):
        raise HTTPException(status_code=400, detail="Invalid CAPTCHA")

    # ✅ Continue with reset flow
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    expire = datetime.utcnow() + timedelta(hours=24)
    token_data = {"sub": user.id, "exp": expire}
    token = jwt.encode(token_data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    send_password_reset_email(email=user.email, first_name=user.first_name, token=token)
    return {"message": "Reset link sent to your email."}


@router.post("/reset-password")
def reset_password(payload: PasswordResetPayload, db: Session = Depends(get_db)):
    # ✅ Turnstile CAPTCHA validation
    verify_url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    data = {
        "secret": settings.TURNSTILE_SECRET_KEY.get_secret_value(),
        "response": payload.turnstile_token,
    }
    resp = requests.post(verify_url, data=data)
    result = resp.json()
    if not result.get("success"):
        raise HTTPException(status_code=400, detail="Invalid CAPTCHA")

    # ✅ Token verification and password update
    try:
        decoded = jwt.decode(payload.token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = decoded.get("sub")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = get_password_hash(payload.password)
    db.commit()

    return {"message": "Password updated successfully"}


@router.get("/me", response_model=UserOut)
def get_current_user_info(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return current_user

