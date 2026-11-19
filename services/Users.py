from sqlalchemy.orm import Session
from schema.auth import CreateUser,LoginUser
from models import Users
from security import hash_password,verify_password
from repository.users import (email_Exist,create_db_user,rep_users,retrive_single,email_exist,update_user,delete)
from exceptions import UserEmailAlreadyExistError,UserNotFoundError,InvalidCredentialsError,InactiveUserError
def service_create_user(user:CreateUser,db:Session):
    hashpassword=hash_password(user.password)
    db_user=Users(username=user.username,email=user.email,password=hashpassword)
    exist=email_Exist(user.email,db)
    if exist is not None:
        raise UserEmailAlreadyExistError()
    return create_db_user(db_user,db)
def service_users(db:Session):
    return rep_users(db)
def service_update_user(id:int,modified:dict,db:Session):
    user=retrive_single(id,db)
    if user is None:
        raise UserNotFoundError()
    exist=email_exist(modified.email,db)
    if exist is not None:
        raise UserEmailAlreadyExistError()
    return update_user(user,modified,db)
def service_delete(id:int,db:Session):
    stmt=retrive_single(id,db)
    if stmt is None:
        raise UserNotFoundError()
    return delete(stmt,db)
def authenticate_user(email:str,password:str,db:Session):
    user=email_Exist(email,db)
    if user is None:
        raise InvalidCredentialsError()
    if not verify_password(password,user.password):
        raise InvalidCredentialsError()
    if not user.is_active:
        raise InactiveUserError()
    return user
    



    