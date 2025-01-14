from fastapi import APIRouter
from models.models import Project
from services.Project_work import project_obj

router1 = APIRouter()

@router1.post("/create_project/")
async def create_project(project: Project):
    return project_obj.create_project(project)

@router1.get("/projects/")
async def get_projects():
    return project_obj.get_projects()

@router1.get("/projects/{project_id}")
async def get_project(project_id: int):
    return project_obj.get_project_by_id(project_id)

@router1.put("/projects/{project_id}")
async def update_project(project_id: int, updated_project: Project):
    return project_obj.update_project(project_id, updated_project)

@router1.delete("/projects/{project_id}")
async def delete_project(project_id: int):
    return project_obj.delete_project(project_id)