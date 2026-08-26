from datetime import datetime, timedelta, timezone
import jwt
def create_access_token(data, secret_key, algorithm="HS256", expires_delta=None):
    payload=data.copy(); payload["exp"]=datetime.now(timezone.utc)+(expires_delta or timedelta(minutes=120))
    return jwt.encode(payload, secret_key, algorithm=algorithm)
def decode_access_token(token, secret_key, algorithm="HS256"): return jwt.decode(token, secret_key, algorithms=[algorithm])
