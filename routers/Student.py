from fastapi import APIRouter,HTTPException
from schema.students import createStudent,UpdateStudent,ResponseStudent
from sqlalchemy.orm import Session
from exceptions import StudentNotFoundError
from database import get_db
from fastapi import HTTPException,Depends,status
from services.Student import Create_student,retrive_All,retrive_single,update_record,delete_record
from sqlalchemy.exc import IntegrityError

router=APIRouter(prefix="/student",tags=["student"])
@router.post("/",response_model=ResponseStudent,status_code=status.HTTP_201_CREATED)

def home(student:createStudent,db:Session=Depends(get_db)):

    return Create_student(student,db)

@router.get("/",response_model=list[ResponseStudent])
def home(db :Session=Depends(get_db)):
    Students=retrive_All(db)
    if not Students:
        raise StudentNotFoundError()
    return Students
@router.get("/{Student_id}",response_model=ResponseStudent)
def root(Student_id:int,db:Session=Depends(get_db)):
    r=retrive_single(Student_id,db)
    if r is None:
        raise StudentNotFoundError()
    return r
'''@router.get("/age/{age}",response_model=list[ResponseStudent])
def hoom(age:int,db:Session=Depends(get_db)):
    stmt=select(Student).where(Student.age>age)
    result=db.execute(stmt)
    records=result.scalars().all()
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"there is no students more than {age}")
    return records'''
@router.put("/{student_id}", response_model=ResponseStudent)
def update_student(
    student_id: int,
    s: UpdateStudent,
    db: Session = Depends(get_db)
):
    re1=s.model_dump(exclude_unset=True)
    return update_record(student_id,re1,s,db)
@router.delete("/{student_id}")
def delete(student_id:int,db:Session=Depends(get_db)):
    return delete_record(student_id,db)
