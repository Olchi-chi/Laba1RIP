import json
import os
from inquirer import prompt, List, Text

# Путь к JSON файлу
DB_FILE = "projects.json"

# Функция для загрузки данных из JSON файла
def load_projects():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as file:
        return json.load(file)

# Функция для сохранения данных в JSON файл
def save_projects(projects):
    with open(DB_FILE, "w") as file:
        json.dump(projects, file, indent=4)

def main():
    projects = load_projects()
    questions = [
        List('action', message="What do you want to do?", choices=['Create', 'Read', 'Update', 'Delete'])
    ]
    answers = prompt(questions)
    action = answers['action']

    if action == 'Create':
        entity = {}
        entity['name'] = prompt([Text('name', message="Enter the name: ", default='Default Name')])['name']
        entity['description'] = prompt([Text('description', message="Enter the description: ", default='Default Description')])['description']
        entity['podrazdelenie'] = prompt([Text('podrazdelenie', message="Enter the podrazdelenie: ", default='Default Podrazdelenie')])['podrazdelenie']
        entity['date'] = prompt([Text('date', message="Enter the date: ", default='2023-10-01')])['date']
        entity['id'] = 1 if not projects else max(p["id"] for p in projects) + 1
        projects.append(entity)
        save_projects(projects)
        print('Entity created successfully!')

    elif action == 'Read':
        entity_id = prompt([Text('id', message="Enter the ID of the entity to read: ")])['id']
        entity = next((p for p in projects if p["id"] == int(entity_id)), None)
        if entity:
            print(f'Entity found: {entity}')
        else:
            print('Entity not found.')

    elif action == 'Update':
        entity_id = prompt([Text('id', message="Enter the ID of the entity to update: ")])['id']
        entity = next((p for p in projects if p["id"] == int(entity_id)), None)
        if entity:
            entity['name'] = prompt([Text('name', message="Enter the new name: ", default=entity['name'])])['name']
            entity['description'] = prompt([Text('description', message="Enter the new description: ", default=entity['description'])])['description']
            entity['podrazdelenie'] = prompt([Text('podrazdelenie', message="Enter the new podrazdelenie: ", default=entity['podrazdelenie'])])['podrazdelenie']
            entity['date'] = prompt([Text('date', message="Enter the new date: ", default=entity['date'])])['date']
            save_projects(projects)
            print('Entity updated successfully!')
        else:
            print('Entity not found.')

    elif action == 'Delete':
        entity_id = prompt([Text('id', message="Enter the ID of the entity to delete: ")])['id']
        entity = next((p for p in projects if p["id"] == int(entity_id)), None)
        if entity:
            projects.remove(entity)
            save_projects(projects)
            print('Entity deleted successfully!')
        else:
            print('Entity not found.')

if __name__ == "__main__":
    main()
