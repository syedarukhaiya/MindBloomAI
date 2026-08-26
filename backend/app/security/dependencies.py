from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.security.jwt import decode_access_token
from app.core.config import settings
bearer_scheme=HTTPBearer(auto_error=True)
def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)], db: Session=Depends(get_db)) -> User:
    try:
        payload=decode_access_token(credentials.credentials, settings.jwt_secret_key, settings.jwt_algorithm)
        uid=payload.get("sub")
        user=db.get(User,int(uid)) if uid is not None else None
        if user is None: raise ValueError
        return user
    except (ExpiredSignatureError, InvalidTokenError, ValueError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired authentication token", headers={"WWW-Authenticate":"Bearer"})
