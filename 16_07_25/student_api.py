from fastapi import FastAPI , Query, Path,HTTPException,Form 
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager
import json
import os

DATA_FILE = "students.json"
login_data="login_details.json"
def save_login_data():
    with open(login_data,"w")as f:
        json.dump(login_set,f,indent=4)

def load_login_data():
    global login_set
    if os.path.exists(login_data):
        with open(login_data,"r")as f:
            login_set.update(json.load(f))

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({k: v.dict() for k, v in student_list.items()}, f, indent=4)

def load_data():
    global student_list, id_count
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            student_list.update({int(k): Student(**v) for k, v in data.items()})
            id_count = max(student_list.keys(), default=0)

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_data()
    load_login_data()
    yield

app = FastAPI (lifespan=lifespan)

login_set={}

@app.post("/signup/")
def signup(
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)
):
    if username in login_set:
        raise HTTPException(status_code=400, detail="Username already exists. Please login.")
    
    login_set[username] = {
        "password": password,
        "role": role
    }
    save_login_data()
    return {
        "message": f"User '{username}' registered successfully!",
        "your_role": role
    }

@app.post("/login/")
def login(
    username : str=Form(...),
    password : str=Form(...),
    role : str=Form(...)
):
    if username not in login_set:
        raise HTTPException (status_code=404,detail=f"Username {username} Not Found, Please Signup First.")  
  
    login_detail=login_set[username]
  
    if login_detail["password"] != password:
        return {"message": "Your password is invalid."}

    if login_detail["role"] != role:
        return {"message": "Role mismatch."}
    
    return {"message": f"Welcome {role.capitalize()} {username}!"}
    

@app.get('/')
def home():
    return "Home Page."

student_list={}
id_count=0

class Student (BaseModel):
    name:str
    age:int
    mark:float

@app.post("/student/")
def get_student(student:Student):
    global id_count

    for s in student_list.values():
        if s.name == student.name:
            return {student.name:"Student Already in database."}
        
    if student.age<18:
        return {"message":"Student Age must be age 18 or more to add.",
                "You Entered student age ":student.age}
    
    if student.mark<50.00:
        return {"message":"Student must 50% mark to add.",
                "You entered student mark": student.mark}
    
    elif student.mark >100.0:
        return {"message":"You entered worrng mark of more than 100%",
                "You entered student mark": student.mark}
        
    
    id_count+=1
    student_list[id_count]=student

    save_data()

    return{
        "message": "Student created successfully!",
        "student_data": student
    }

@app.get("/student/{student_id}")
def get_studend(
        student_id:int,
        show:Optional[str]=None   
):
    if student_id not in student_list:
        raise HTTPException(status_code=404,detail=f"Studernt ID :{student_id} Not Found. ")
    
    student_detail=student_list[student_id]

    if show == "profile":
        return {
            "Name":student_detail.name,
            "age":student_detail.age
            }
    elif show == "mark":
        return {"Mark":student_detail.mark}
    else:
        return student_detail

@app.put("/student/{student_id}")
def update(
    student_id: int,
    name: Optional[str] = Query(None),
    age: Optional[int] = Query(None),
    mark: Optional[float] = Query(None)
):

    if student_id not in student_list:
        raise HTTPException(status_code=404,detail=f"Studernt ID :{student_id} Not Found. ")
    
    student = student_list[student_id]
    if name:
        student.name=name
    if age:
        if age<18:
            return {
                "message": "Student age must be 18 or more.",
                "Entered age": student.age
            }
        student.age=age
    if mark:
        if mark < 50 or mark > 100:
            return {"message": "Marks must be between 50 and 100."}
        student.mark = mark

    save_data()

    return {
        "message": f"Student ID {student_id} updated successfully via query params.",
        "Old_data": "Removed from the database.",
        "updated_data": student
    }

@app.delete("/student/{student_id}")
def delete_student(student_id:int):
    if student_id not in student_list:
        raise HTTPException(status_code=404,detail=f"Student ID :{student_id} Not Found.")
    
    deleted_student=student_list.pop(student_id)

    save_data()

    return {
        "message": f"Student ID {student_id} deleted successfully.",
        "deleted_data": deleted_student
    }