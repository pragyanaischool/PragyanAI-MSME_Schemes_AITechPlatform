from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

pwd_hasher = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials or expired session",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise exc
    except jwt.PyJWTError:
        raise exc
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise exc
    return user

@router.post("/register", response_model=schemas.TokenResponse)
def register(user_in: schemas.UserRegister, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Account with this email already exists")

    user = models.User(
        email=user_in.email,
        hashed_password=pwd_hasher.hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role.lower(),
        jurisdiction=user_in.jurisdiction or "Karnataka"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id), "role": user.role, "jurisdiction": user.jurisdiction})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "jurisdiction": user.jurisdiction,
        "user_id": str(user.id),
        "full_name": user.full_name
    }

@router.post("/login", response_model=schemas.TokenResponse)
def login(creds: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == creds.email).first()
    if not user or not pwd_hasher.verify(creds.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id), "role": user.role, "jurisdiction": user.jurisdiction})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "jurisdiction": user.jurisdiction,
        "user_id": str(user.id),
        "full_name": user.full_name
    }
