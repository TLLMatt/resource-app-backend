# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import asyncpg
import os
import uvicorn

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase PostgreSQL connection
DATABASE_URL = "postgresql://postgres:TechLabsMatt31?!@db.dzifhyukbvkibarpthtj.supabase.co:5432/postgres"

@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.create_pool(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

# Models
class Resource(BaseModel):
    id: int
    name: str
    role: str
    availability: str
    status: str

class NewResource(BaseModel):
    name: str
    role: str
    availability: str
    status: str

class Project(BaseModel):
    id: int
    name: str
    start_date: str
    end_date: str
    status: str

class NewProject(BaseModel):
    name: str
    start_date: str
    end_date: str
    status: str

# Routes
@app.get("/resources", response_model=List[Resource])
async def get_resources():
    rows = await app.state.db.fetch("SELECT * FROM resources ORDER BY id")
    return [dict(row) for row in rows]

@app.post("/resources", response_model=Resource)
async def create_resource(resource: NewResource):
    query = """
        INSERT INTO resources (name, role, availability, status)
        VALUES ($1, $2, $3, $4)
        RETURNING *
    """
    row = await app.state.db.fetchrow(query, resource.name, resource.role, resource.availability, resource.status)
    return dict(row)

@app.get("/projects", response_model=List[Project])
async def get_projects():
    rows = await app.state.db.fetch("SELECT * FROM projects ORDER BY id")
    return [dict(row) for row in rows]

@app.post("/projects", response_model=Project)
async def create_project(project: NewProject):
    query = """
        INSERT INTO projects (name, start_date, end_date, status)
        VALUES ($1, $2, $3, $4)
        RETURNING *
    """
    row = await app.state.db.fetchrow(query, project.name, project.start_date, project.end_date, project.status)
    return dict(row)

# Entry point
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
