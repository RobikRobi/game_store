import jwt
import bcrypt
from src.config import configtoken
import datetime
from fastapi import HTTPException

# хэширование пароля
async def encode_password(password: str) -> bytes:
    if not password:
        raise ValueError("Password cannot be empty")
    new_password = bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())
    return new_password

# проверка пароля
async def check_password(password: str, old_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=old_password)

# создание токена
async def create_access_token(
    user_id: int,
    algorithm: str = configtoken.algorithm,
    private_key: str = configtoken.private_key.read_text()
) -> str:
    payload = {
        "user_id": user_id,
        "exp": (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=configtoken.days)).timestamp()}
    
    access_token = jwt.encode(payload=payload, algorithm=algorithm, key=private_key)
    return access_token


async def valid_access_token(
    token: str, 
    algorithm: str = configtoken.algorithm,
    public_key: str = configtoken.public_key.read_text()
) -> int:
    try:
        payload = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

    exp = payload.get("exp")
    if exp and exp < datetime.datetime.now(datetime.timezone.utc).timestamp():
        raise HTTPException(status_code=401, detail="Token has expired.")
    
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token: missing user_id")
    
    return user_id