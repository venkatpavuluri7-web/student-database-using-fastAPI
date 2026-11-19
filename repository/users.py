from sqlalchemy import Select
from sqlalchemy.orm import Session
from models import Users
from sqlalchemy.exc import IntegrityError
def email_Exist(email:str,db:Session):
    stmt=Select(Users).where(Users.email==email)
    return db.execute(stmt).scalars().first()
def create_db_user(db_user:Users,db:Session):
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise
def rep_users(db:Session):
    stmt=Select(Users)
    return db.execute(stmt).scalars().all()
def retrive_single(id:int,db:Session):
    stmt=Select(Users).where(Users.id==id)
    return db.execute(stmt).scalars().first()
def email_exist(email:str,db:Session):
    stmt=Select(Users).where(Users.email==email)
    return db.execute(stmt).scalars().first()
def update_user(user:Users,modified:dict,db:Session):
    for key,item in modified.items():
        setattr(user,key,item)
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise
def delete(record:Users,db:Session):
    try:
       db.delete(record)
       db.commit()
       return {"message":f"{record} is deleted successfull"}
    except Exception:
        raise
