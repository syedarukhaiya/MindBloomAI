from sqlalchemy import select
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import RegisterRequest,LoginRequest
from app.security.jwt import create_access_token
hasher=PasswordHasher()
def register_user(db:Session,data:RegisterRequest):
 if db.scalar(select(User).where(User.email==data.email)): raise ValueError("Email already registered")
 if db.scalar(select(User).where(User.username==data.username)): raise ValueError("Username already registered")
 u=User(email=data.email,username=data.username,password_hash=hasher.hash(data.password)); db.add(u); db.commit(); db.refresh(u); return u
def authenticate_user(db:Session,data:LoginRequest):
 u=db.scalar(select(User).where(User.email==data.email))
 if not u:
  raise ValueError("Invalid email or password")
 try:
  hasher.verify(u.password_hash,data.password)
 except VerifyMismatchError:
  raise ValueError("Invalid email or password")
 return u
def token_for(u): return create_access_token({"sub":str(u.id),"email":u.email},settings.jwt_secret_key,settings.jwt_algorithm)
