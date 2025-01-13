from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class Project(BaseModel):
    id: int
    name: str
    description: str = None
    date: str
    podrazdelenie: str

@app.post("/projects/")
async def create_project(project: Project):
    return project

@app.get("/projects/{project_id}")
async def read_project(project_id: int):
    return {"project_id": project_id}

@app.put("/projects/{project_id}")
async def update_project(project_id: int, project: Project):
    return {"project_id": project_id, "project": project}

@app.delete("/projects/{project_id}")
async def delete_project(project_id: int):
    return {"message": "Project deleted", "project_id": project_id}