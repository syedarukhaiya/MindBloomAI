@router.post(
    "/auth/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    try:
        user = register_user(db, data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return TokenResponse(
        access_token=token_for(user),
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/auth/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    try:
        user = authenticate_user(db, data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return TokenResponse(
        access_token=token_for(user),
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )