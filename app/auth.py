from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from .database import user_collection
from .models import user_helper
import os

# ✅ Password Hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ JWT Config
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ✅ Hash Password
def hash_password(password: str):
    return pwd_context.hash(password)

# ✅ Verify Password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ✅ Create JWT Token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ✅ Decode JWT Token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ✅ Get Current User from Token (Used as Dependency)
def get_current_user(token: str = Depends(lambda: None)):
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")
    payload = decode_access_token(token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token data")
    user = user_collection.find_one({"username": username})
    if user:
        return user_helper(user)
    raise HTTPException(status_code=404, detail="User not found")
