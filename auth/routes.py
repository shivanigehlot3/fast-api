from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.auth import schemas, utils, models
from datetime import datetime, timezone, timedelta

from app.utils.email_utils import send_reset_email


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
def signup(user: schemas.SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = utils.hash_password(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Signup successful"}

@router.post("/signin", response_model=schemas.TokenResponse)
def signin(user: schemas.SigninRequest, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {"sub": str(db_user.id), "role": db_user.role}
    access_token = utils.create_access_token(payload)
    refresh_token = utils.create_refresh_token(payload)

    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/forgot-password")
def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = utils.generate_reset_token()
    expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    reset = models.PasswordResetToken(
        user_id=user.id,
        token=token,
        expiration_time=expires.isoformat(),
        used="false"
    )
    db.add(reset)
    db.commit()

    #email sending --> reset
    send_reset_email(request.email, token)

    return {"message": "Reset token sent to your email."}

@router.post("/reset-password")
def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    token_entry = db.query(models.PasswordResetToken).filter(
        models.PasswordResetToken.token == request.token,
        models.PasswordResetToken.used == "false"
    ).first()

    if not token_entry:
        raise HTTPException(status_code=404, detail="Invalid or expired token")

    if datetime.fromisoformat(token_entry.expiration_time) < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Token expired")

    user = db.query(models.User).filter(models.User.id == token_entry.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = utils.hash_password(request.new_password)
    token_entry.used = "true"
    db.commit()
    return {"message": "Password reset successful"}
