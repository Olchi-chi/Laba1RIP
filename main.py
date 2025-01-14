from fastapi import FastAPI
from project_router import router1

app = FastAPI()
app.include_router(router1)