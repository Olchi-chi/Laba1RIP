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

# Модель данных
class Project(BaseModel):
    id: int = None
    name: str
    description: str
    podrazdelenie: str
    date: str

# Путь к JSON файлу
DB_FILE = "projects.json"

# Функция для загрузки данных из JSON файла
def load_projects():
    try:
        with open(DB_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Функция для сохранения данных в JSON файл
def save_projects(projects):
    with open(DB_FILE, "w") as file:
        json.dump(projects, file, indent=4)

# Маршрут для получения всех проектов
@app.get("/projects", response_model=List[Project])
def get_projects():
    projects = load_projects()
    return projects

# Маршрут для получения проекта по ID
@app.get("/projects/{project_id}", response_model=Project)
def get_project(project_id: int):
    projects = load_projects()
    for project in projects:
        if project["id"] == project_id:
            return project
    raise HTTPException(status_code=404, detail="Project not found")

# Маршрут для добавления нового проекта
@app.post("/projects", response_model=Project)
def create_project(project: Project):
    print("Received project data:", project)
    projects = load_projects()
    new_id = 1 if not projects else max(p["id"] for p in projects) + 1
    new_project = project.dict()
    new_project["id"] = new_id
    projects.append(new_project)
    save_projects(projects)
    return new_project

# Маршрут для редактирования проекта
@app.put("/projects/{project_id}", response_model=Project)
def update_project(project_id: int, updated_project: Project):
    projects = load_projects()
    for project in projects:
        if project["id"] == project_id:
            project.update(updated_project.dict())
            save_projects(projects)
            return project
    raise HTTPException(status_code=404, detail="Project not found")

# Маршрут для удаления проекта
@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    projects = load_projects()
    initial_length = len(projects)
    projects = [p for p in projects if p["id"] != project_id]
    if len(projects) == initial_length:
        raise HTTPException(status_code=404, detail="Project not found")
    save_projects(projects)
    return {"detail": "Project deleted"}

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

# Запуск сервера
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8470)
