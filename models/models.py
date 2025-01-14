from pydantic import BaseModel

# Модель пользователя
class Project(BaseModel):
    id: int
    name: str
    description: str
    podrazdelenie: str
    date: str
