from fastapi import APIRouter
from .endpoints import user as UserRouter

Router = APIRouter()
Router.include_router(UserRouter.router, prefix="/users", tags=["users"])
