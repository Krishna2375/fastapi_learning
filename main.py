from fastapi import FastAPI , Path ,Query,HTTPException
from typing import Optional

app=FastAPI()

students = {
    1: {"name": "Krishna", "age": 20, "marks": {"math": 95, "english": 88}},
    2: {"name": "Ravi", "age": 21, "marks": {"math": 76, "english": 90}},
    3: {"name": "Anjali", "age": 19, "marks": {"math": 82, "english": 85}},
}

@app.get("/")
def home():
    return "Home Page"

@app.get("/student/{student_id}")
def get_studend(
        student_id:int,
        show:Optional[str]=None   #optional query is for show the student 'mark' or 'profile'
):
    if student_id not in students:
        raise HTTPException(status_code=404,detail=f"Student with {student_id} ID not found.")
    student=students[student_id]

    if show == "marks":
        return {"Marks": student["marks"]}
    elif show == "profile":
        return {"Name": student['name'], "age": student['age']}
    else:
        return student
    
@app.get("/student/{student_id}/details")
def get_student_fields(
        student_id:int,
        fields:Optional[list[str]]= Query(None)
):
    if student_id not in students:
        raise HTTPException(status_code=404,detail=f"Student with {student_id} ID not found.")
    student=students[student_id]

    if not fields:
        return student
    
    result={}

    for field in fields:
        if field in student:
            result[field]=student[field]
        elif field=="marks":
            result["marks"]=student.get("mark")
    return result