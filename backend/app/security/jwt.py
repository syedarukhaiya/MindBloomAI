from datetime import datetime, timedelta, timezone

import jwt


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(
    data: dict,
    secret_key: str,
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()

    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        secret_key,
        algorithm=ALGORITHM,
    )


def decode_access_token(
    token: str,
    secret_key: str,
) -> dict:
    return jwt.decode(
        token,
        secret_key,
        algorithms=[ALGORITHM],
    )
