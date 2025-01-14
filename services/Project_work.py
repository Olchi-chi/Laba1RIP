from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from random import randint
import json
import os
from models.models import Project
app = FastAPI()

file = "database/projects.json"

class ProjectWork:

    def create_project(self, project: Project):
        try:
            # Проверяем, существует ли файл
            if not os.path.exists(file):
                raise HTTPException(status_code=404, detail="Файл не найден.")

            # Открываем файл с проектами
            with open(file, 'r+') as file_project:
                try:
                    # Загружаем существующие проекты
                    projects = json.load(file_project)
                except json.JSONDecodeError:
                    # Если файл пуст или имеет неправильный формат, создаем пустой список
                    projects = []

                new_id = self.generate_unique_id(projects)

                # Создаем новый проект как словарь
                new_project = {
                    'id': new_id,
                    'name': project.name,
                    'description': project.description,
                    'podrazdelenie': project.podrazdelenie,
                    'date': project.date
                }
                projects.append(new_project)

                # Перезаписываем файл с обновленным списком проектов
                file_project.seek(0)
                file_project.truncate()
                json.dump(projects, file_project, indent=4)

            return {'status': 200, 'content': 'Проект был добавлен.'}

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')

    def generate_unique_id(self, projects):
        new_id = randint(1, 10000)

        # Проверка на уникальность ID
        while any(p['id'] == new_id for p in projects):
            new_id = randint(1, 10000)

        return new_id
    
    def get_projects(self):
        try:
            if not os.path.exists(file):
                raise HTTPException(status_code=404, detail="Файл не найден.")

            with open(file, 'r') as file_project:
                try:
                    projects = json.load(file_project)
                    return {'status': 200, 'projects': projects}
                except json.JSONDecodeError:
                    return {'status': 200, 'projects': []}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')

    def get_project_by_id(self, project_id: int):
        try:
            if not os.path.exists(file):
                raise HTTPException(status_code=404, detail="Файл не найден.")

            with open(file, 'r') as file_project:
                projects = json.load(file_project)

            project = next((p for p in projects if p['id'] == project_id), None)
            if project is None:
                raise HTTPException(status_code=404, detail="Проект не найден.")
            
            return {'status': 200, 'project': project}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')

    def update_project(self, project_id: int, updated_project: Project):
        try:
            if not os.path.exists(file):
                raise HTTPException(status_code=404, detail="Файл не найден.")

            with open(file, 'r+') as file_project:
                projects = json.load(file_project)

                project = next((p for p in projects if p['id'] == project_id), None)
                if project is None:
                    raise HTTPException(status_code=404, detail="Проект не найден.")

                # Обновляем данные проекта
                project.update({
                    'name': updated_project.name,
                    'description': updated_project.description,
                    'podrazdelenie': updated_project.podrazdelenie,
                    'date': updated_project.date
                })

                # Перезаписываем файл с обновленным списком проектов
                file_project.seek(0)
                file_project.truncate()
                json.dump(projects, file_project, indent=4)

            return {'status': 200, 'content': 'Проект был обновлен.'}

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')

    def delete_project(self, project_id: int):
        try:
            if not os.path.exists(file):
                raise HTTPException(status_code=404, detail="Файл не найден.")

            with open(file, 'r+') as file_project:
                projects = json.load(file_project)

                project = next((p for p in projects if p['id'] == project_id), None)
                if project is None:
                    raise HTTPException(status_code=404, detail="Проект не найден.")

                # Удаляем проект из списка
                projects.remove(project)

                # Перезаписываем файл с обновленным списком проектов
                file_project.seek(0)
                file_project.truncate()
                json.dump(projects, file_project, indent=4)

            return {'status': 200, 'content': 'Проект был удален.'}

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')

project_obj = ProjectWork()

