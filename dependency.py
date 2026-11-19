from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from database import get_db
from config import settings
from repository.users import retrive_single


oauth2schema = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)


def get_current_user(
    token: str = Depends(oauth2schema),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        print("PAYLOAD:", payload)

        user_id = payload.get("sub")

        print("USER ID:", user_id)

        if user_id is None:
            print("SUB IS MISSING")
            raise credentials_exception

    except JWTError as e:

        print("JWT ERROR:", e)
        raise credentials_exception

    user = retrive_single(
        int(user_id),
        db
    )

    print("USER:", user)

    if user is None:
        print("USER NOT FOUND")
        raise credentials_exception

    if not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user
def require_admin(current_user=Depends(get_current_user)):
    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="admin access is required")
    return current_user