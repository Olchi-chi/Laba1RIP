from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import uvicorn

app = FastAPI()

# Настройки CORS
origins = [
    "http://localhost:3000",  # URL вашего фронтенда
    "http://127.0.0.1:3000"  # URL вашего фронтенда
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель данных для проектов
class Project(BaseModel):
    id: int = None
    name: str
    description: str
    podrazdelenie: str
    date: str

# Модель данных для навыков
class Skill(BaseModel):
    id: int = None
    name: str
    description: str

# Путь к JSON файлам
PROJECTS_DB_FILE = "projects.json"
SKILLS_DB_FILE = "skills.json"

# Функция для загрузки данных из JSON файла
def load_data(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Функция для сохранения данных в JSON файл
def save_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Маршруты для проектов
@app.get("/projects", response_model=List[Project])
def get_projects():
    projects = load_data(PROJECTS_DB_FILE)
    return projects

@app.get("/projects/{project_id}", response_model=Project)
def get_project(project_id: int):
    projects = load_data(PROJECTS_DB_FILE)
    for project in projects:
        if project["id"] == project_id:
            return project
    raise HTTPException(status_code=404, detail="Project not found")

@app.post("/projects", response_model=Project)
def create_project(project: Project):
    projects = load_data(PROJECTS_DB_FILE)
    new_id = 1 if not projects else max(p["id"] for p in projects) + 1
    new_project = project.dict()
    new_project["id"] = new_id
    projects.append(new_project)
    save_data(PROJECTS_DB_FILE, projects)
    return new_project

@app.put("/projects/{project_id}", response_model=Project)
def update_project(project_id: int, updated_project: Project):
    projects = load_data(PROJECTS_DB_FILE)
    for project in projects:
        if project["id"] == project_id:
            project.update(updated_project.dict())
            save_data(PROJECTS_DB_FILE, projects)
            return project
    raise HTTPException(status_code=404, detail="Project not found")

@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    projects = load_data(PROJECTS_DB_FILE)
    initial_length = len(projects)
    projects = [p for p in projects if p["id"] != project_id]
    if len(projects) == initial_length:
        raise HTTPException(status_code=404, detail="Project not found")
    save_data(PROJECTS_DB_FILE, projects)
    return {"detail": "Project deleted"}

# Маршруты для навыков
@app.get("/skills", response_model=List[Skill])
def get_skills():
    skills = load_data(SKILLS_DB_FILE)
    return skills

@app.get("/skills/{skill_id}", response_model=Skill)
def get_skill(skill_id: int):
    skills = load_data(SKILLS_DB_FILE)
    for skill in skills:
        if skill["id"] == skill_id:
            return skill
    raise HTTPException(status_code=404, detail="Skill not found")

@app.post("/skills", response_model=Skill)
def create_skill(skill: Skill):
    skills = load_data(SKILLS_DB_FILE)
    new_id = 1 if not skills else max(s["id"] for s in skills) + 1
    new_skill = skill.dict()
    new_skill["id"] = new_id
    skills.append(new_skill)
    save_data(SKILLS_DB_FILE, skills)
    return new_skill

@app.put("/skills/{skill_id}", response_model=Skill)
def update_skill(skill_id: int, updated_skill: Skill):
    skills = load_data(SKILLS_DB_FILE)
    for skill in skills:
        if skill["id"] == skill_id:
            skill.update(updated_skill.dict())
            save_data(SKILLS_DB_FILE, skills)
            return skill
    raise HTTPException(status_code=404, detail="Skill not found")

@app.delete("/skills/{skill_id}")
def delete_skill(skill_id: int):
    skills = load_data(SKILLS_DB_FILE)
    initial_length = len(skills)
    skills = [s for s in skills if s["id"] != skill_id]
    if len(skills) == initial_length:
        raise HTTPException(status_code=404, detail="Skill not found")
    save_data(SKILLS_DB_FILE, skills)
    return {"detail": "Skill deleted"}

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Запуск сервера
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8470)
