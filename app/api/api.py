from fastapi import APIRouter
from api.routes import task_routes
from api.routes import user_routes

api_router = APIRouter()
api_router.include_router(task_routes.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(user_routes.router, prefix="/users", tags=["users"])
