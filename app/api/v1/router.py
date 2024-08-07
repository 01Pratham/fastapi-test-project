from fastapi import APIRouter
from .endpoints import user as UserRouter
from .endpoints import posts as PostsRouter

Router = APIRouter()
Router.include_router(UserRouter.router, prefix="/users", tags=["users"])
Router.include_router(PostsRouter.router, prefix="/posts", tags=["Posts"])
