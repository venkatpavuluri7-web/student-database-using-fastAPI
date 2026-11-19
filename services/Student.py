from schema.students import createStudent,UpdateStudent
from sqlalchemy.orm import Session
from repository.Student import studentrepository
from sqlalchemy import select
from exceptions import StudentNotFoundError,StudentEmailAlreadyExistError
from sqlalchemy.exc import IntegrityError
from models import Student
def Create_student(student_data:createStudent,db:Session):
    db_student=Student(name=student_data.name,age=student_data.age,email=student_data.email,phoneNumber=student_data.phoneNumber)
    exist=studentrepository.email_exist(student_data.email,db)
    if exist is not None:
            raise StudentEmailAlreadyExistError()
    return studentrepository.create_student(db_student,db)
def retrive_All(db:Session):
    return studentrepository.retriveAll(db)
def retrive_single(id:int,db:Session):
    return studentrepository.retriveSingle(id,db)
def update_record(id:int,re1:dict,record:UpdateStudent,db:Session):
    re=studentrepository.retriveSingle(id,db)
    if re is None:
        raise StudentNotFoundError()
    exist=studentrepository.email_exist(record.email,db)
    if exist is not None:
        raise StudentEmailAlreadyExistError()
    return studentrepository.update_Student(re1, re, db)
def delete_record(id:int,db:Session):
    re=studentrepository.retriveSingle(id,db)
    if re is None:
        raise StudentNotFoundError()
    studentrepository.delete_student(re,db)
    return {"message":f"{re} is deleted successfull"}