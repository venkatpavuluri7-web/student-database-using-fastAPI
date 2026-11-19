from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from exceptions import StudentNotFoundError,StudentEmailAlreadyExistError,UserEmailAlreadyExistError,UserNotFoundError,InactiveUserError,InvalidCredentialsError
from routers.Student import router as student_routers
from routers.Users import router as User_Routers
app=FastAPI(
    title="student management api",description="fastapi crud application with themysql",version="1.0.0"
)
app.include_router(student_routers)
app.include_router(User_Routers)
@app.exception_handler(StudentNotFoundError)
def student_not_found(request:Request,exc:StudentNotFoundError):
    return JSONResponse(status_code=404, content={"detail":"student not found"})
@app.exception_handler(UserNotFoundError)
def student_not_found(request:Request,exc:UserNotFoundError):
    return JSONResponse(status_code=404, content={"detail":"userS not found"})
@app.exception_handler(StudentEmailAlreadyExistError)
def EmailAlreadyExist(request:Request,exc:StudentEmailAlreadyExistError):
    return JSONResponse(status_code=400,content={"detail":"email already exists"})
@app.exception_handler(UserEmailAlreadyExistError)
async def user_email_exist(request:Request,exc:UserEmailAlreadyExistError):
    return JSONResponse(status_code=400,content={"details":"email already exists"})
@app.exception_handler(InactiveUserError)
async def inactive_user(request:Request,exc:InactiveUserError):
    return JSONResponse(status_code=404,content={"details":"inactive user"})
@app.exception_handler(InvalidCredentialsError)
async def inactive_user(request:Request,exc:InvalidCredentialsError):
    return JSONResponse(status_code=401,content={"details":"invalid email or ppassword"})
'''@app.exception_handler(Exception)
def general_exception_handler(request:Request,exc:Exception):
    return JSONResponse(status_code=500,content={"detail":"internal server     error"})
'''
@app.get("/")
def hoom():
    return {"message": "running on the mysql server"}