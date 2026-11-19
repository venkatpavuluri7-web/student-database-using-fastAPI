import bcrypt
from uuid import uuid4
from datetime import timedelta,timezone,datetime
from config import settings
from jose import jwt,JWTError
def hash_password(password:str):
    salt=bcrypt.gensalt()
    pwd_bytes=password.encode('utf-8')
    hashed_password=bcrypt.hashpw(pwd_bytes,salt)
    return hashed_password.decode('utf-8')
def verify_password(plain_password:str,hashed_password:str):
    plain_bytes=plain_password.encode('utf-8')
    hased_bytes=hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_bytes,hased_bytes)
def create_access_token(
        user_id:int,role:str,
        expires_time:timedelta|None=None
):
    if expires_time is None:
        expires_time=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    expire=datetime.now(timezone.utc)+expires_time
    payload={"sub":str(user_id),
             "role":role,
             "type":"access",
             "exp":expire
             }
    encoded_jwt=jwt.encode(payload,
                          settings.JWT_SECRET_KEY,
                          algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt
def create_refresh_token(user_id:int)->tuple[str,str]:
    token_id=str(uuid4())
    expire=datetime.now(timezone.utc)+timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    payload={"sub":str(user_id),
             "type":"refresh",
             "jti":token_id,
             "exp":expire}
    token=jwt.encode(payload,
                      settings.JWT_SECRET_KEY,
                      algorithm=settings.JWT_ALGORITHM)
    return token,token_id
def decode_refresh_token(refresh_token:str):
    try:
        payload=jwt.decode(refresh_token,
                      settings.JWT_SECRET_KEY,
                      algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type")!="refresh":
             return None
        user_id=payload.get("sub")
        token_id=payload.get("jti")
        if user_id is None or token_id is None:
            return None
        return {"user_id":int(user_id),"token_id":token_id}
    except (JWTError,TypeError,ValueError) as e:
        print(f"token decode error {e}")
        return None
    
    
