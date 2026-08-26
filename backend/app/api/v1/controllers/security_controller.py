from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.auth import UserResponse
from app.security.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return UserResponse.model_validate(current_user)
