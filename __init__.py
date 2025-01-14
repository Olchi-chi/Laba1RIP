from fastapi import APIRouter

from Laba1RIP.project_router import router1 as project_router

router = APIRouter()

router.include_router(project_router)