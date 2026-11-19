from fastapi import APIRouter,Depends,HTTPException
from schema.auth import (CreateUser, ResponseUser, UpdateUser,TokenResponse,RefreshTokenRequest)
from sqlalchemy.orm import Session
from database import get_db
from config import settings
from datetime import datetime,timezone,timedelta
from exceptions import UserNotFoundError,InactiveUserError
from repository.users import retrive_single
from repository.refresh_token import insert_token,get_tokenby_gti,revoke_refresh_token
from services.Users import service_create_user,service_users,service_update_user,service_delete,authenticate_user
from security import create_access_token,create_refresh_token,decode_refresh_token
from dependency import get_current_user,require_admin
from fastapi.security import OAuth2PasswordRequestForm
from models import RefreshToken
router=APIRouter(prefix="/users",tags=["users"])
@router.post("/register",response_model=ResponseUser,status_code=201)
def register_user(user:CreateUser,db:Session=Depends(get_db)):
    return service_create_user(user,db)
@router.get("/",response_model=list[ResponseUser])
def get_users(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return service_users(db)
@router.put("/user/{id}",response_model=ResponseUser)
def update_user(id:int,record:UpdateUser,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    modified=record.model_dump(exclude_unset=True)
    return service_update_user(id,modified,db)
@router.delete("/delete/{id}")
def home(id:int,db:Session=Depends(get_db),current_user=Depends(require_admin)):
    return service_delete(id,db)
@router.post("/login",response_model=TokenResponse)
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=authenticate_user(form_data.username,form_data.password,db)
    access_token=create_access_token(user.id,user.role)
    refresh_token,token_id=create_refresh_token(user.id)
    expire=(datetime.now(timezone.utc)
    +timedelta(
        days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS))
    data=RefreshToken(user_id=user.id,token_id=token_id,expire_at=expire,revokeed=False)
    insert_token(db,data)
    return {"access_token":access_token,
            "refresh_token":refresh_token,
            "token_type":"bearer"}
@router.get("/me",response_model=ResponseUser)
def get_my_profile(current_user=Depends(get_current_user)):
    return current_user
@router.post("/refresh",response_model=TokenResponse)
def new_access_token(token_data:RefreshTokenRequest,db:Session=Depends(get_db)):
    decoded=decode_refresh_token(token_data.refresh_token)
    if decoded is None:
        raise HTTPException(status_code=401,detail="inavlid refresh token")
    user_id=decoded.get("user_id")
    token_id=decoded.get("token_id")
    if user_id is None or token_id is None:
        raise HTTPException(status_code=401,detail="invalid refresh token")
    token=get_tokenby_gti(db,token_id)
    if token is None:
        raise HTTPException(status_code=401,detail="token is not found")
    if token.revokeed:
        raise HTTPException(
            status_code=401,
            detail="Refresh token has been revoked"
        )
    user=retrive_single(user_id,db)
    if user is None:
        raise UserNotFoundError()
    if not user.is_active:
        raise InactiveUserError()
    revoke_refresh_token(db,token)
    expire=(datetime.now(timezone.utc)+timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS))
    new_refresh_token,new_token_id=create_refresh_token(user_id)
    data=RefreshToken( user_id=user_id,
    token_id=new_token_id,
    expire_at=expire,
    revokeed=False)
    insert_token(db,data)
    access_token=create_access_token(user.id,user.role)
    return {"access_token":access_token,
            "refresh_token":new_refresh_token,
            "token_type":"bearer"}
@router.post("/logout",response_model=None)
def user_logout(refresh_token1:RefreshTokenRequest,db:Session=Depends(get_db)):
    decode=decode_refresh_token(refresh_token1.refresh_token)
    if decode is None:
        raise HTTPException(status_code=401,detail="invalid access token")
    stored_token=get_tokenby_gti(db,decode["token_id"])
    if stored_token is None:
        return {"message":"logged out"}
    revoke_refresh_token(db,stored_token)
    return {"message":"logged out"}



