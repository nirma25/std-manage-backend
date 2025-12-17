from typing import Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()  # Uses uvicorn server

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allows all origins
    allow_methods=["*"],
    allow_headers=["*"],
)


class Student(BaseModel):  # pydantic
    student_id: int
    name: str
    age: int


students_dict: Dict[int, Student] = {
    1: Student(student_id=1, name="Nimal", age=19),
    2: Student(student_id=2, name="Kamal", age=20)
}


@app.get("/")  # endpoint
def say_hello():
    # Types converted since pydantic used
    student = Student(student_id=453, name="Nimal", age=19)
    return student  # fastapi smart enough to convert python object to json


@app.get("/students")
def get_students():
    return list(students_dict.values())


@app.post("/students")
def create_student(student: Student):
    students_dict[student.student_id] = student
    return {"message": "Successfully created student", "Student": student}


@app.get("/students/{student_id}")  # path parameter
def get_student_by_id(student_id: int):
    return students_dict.get(student_id)  # Returns None if no student is found


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if student_id not in students_dict.keys():
        raise HTTPException(status_code=404, detail="Student ID not found")

    students_dict[student_id] = student

    return {"message": "Student updated successfully", "student": student}


@app.delete("/students/{student_id}")
def del_student(student_id: int):
    if student_id not in students_dict.keys():
        raise HTTPException(status_code=404, detail="Student ID not found")

    deleted_student = students_dict.pop(student_id)

    return {"message": "Student deleted successfully", "student": deleted_student}
