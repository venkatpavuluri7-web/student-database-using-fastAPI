from sqlalchemy import Column,Integer,String,Boolean,DateTime,ForeignKey
from database import Base
from datetime import datetime,timezone
class Student(Base):
    __tablename__="students"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(100),nullable=False)
    age=Column(Integer,nullable=False)
    email=Column(String(100),nullable=False,unique=True)
    phoneNumber=Column(String(15),nullable=True)
class Users(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,autoincrement=True)
    username=Column(String(100),nullable=False,unique=True)
    email=Column(String(100),nullable=False,unique=True)
    password=Column(String(100),nullable=False)
    is_active=Column(Boolean,default=True,nullable=False)
    role=Column(String(50),nullable=False,default="user")
class RefreshToken(Base):
    __tablename__="refreshtoken"
    id=Column(Integer,primary_key=True,autoincrement=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    token_id=Column(String(64),unique=True,nullable=False)
    expire_at=Column(DateTime,nullable=False)
    created_at=Column(DateTime,default=datetime.now(timezone.utc),nullable=False)
    revokeed=Column(Boolean,default=False,nullable=False)