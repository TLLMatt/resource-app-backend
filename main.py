from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock Data
resources = [
    {"id": 1, "name": "John Smith", "role": "Developer", "availability": "Full-Time", "status": "Busy"},
    {"id": 2, "name": "Jane Doe", "role": "Designer", "availability": "Part-Time", "status": "Available"}
]

projects = [
    {"id": 1, "name": "Project Alpha", "start_date": "2024-06-01", "end_date": "2024-08-01", "status": "Active"}
]

tasks = [
    {"id": 1, "project_id": 1, "name": "Design Homepage", "start_date": "2024-06-10", "end_date": "2024-06-20", "required_role": "Designer", "status": "Unassigned"}
]

assignments = []

# Models
class Assignment(BaseModel):
    user_id: int
    task_id: int
    assigned_from: datetime.date
    assigned_to: datetime.date

# Routes
@app.get("/resources")
def get_resources():
    return resources

@app.get("/projects")
def get_projects():
    return projects

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/assign")
def assign_task(assignment: Assignment):
    assignments.append(assignment.dict())
    return {"message": "Assignment successful", "data": assignment}

@app.get("/assignments")
def get_assignments():
    return assignments
