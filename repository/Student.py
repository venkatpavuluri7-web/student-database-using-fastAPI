from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Student

class StudentRepository:
    def create_student(self,db_student:Student,db:Session):

        db.add(db_student)
        try:
            db.commit()
            db.refresh(db_student)
        except IntegrityError:
            db.rollback()
            raise 
        return db_student
    def email_exist(self,email:EmailStr,db:Session):
        stmt=select(Student).where(Student.email==email)
        re=db.execute(stmt).scalars().first()
        return re
    def retriveAll(self,db:Session):
        stmt=select(Student)
        re=db.execute(stmt).scalars().all()
        return re
    def retriveSingle(self,id:int,db:Session):
        stmt=select(Student).where(Student.id==id)
        re1=db.execute(stmt).scalars().first()
        return re1
    def update_Student(self,sorted:dict,student:Student,db:Session):
        for key,value in sorted.items():
            setattr(student,key,value)
        try:
            db.commit()
            db.refresh(student)
            return student
        except IntegrityError:
            db.rollback()
            raise
    def delete_student(self,student:Student,db:Session):
            db.delete(student)
            db.commit()
studentrepository=StudentRepository()
