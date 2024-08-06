from fastapi import APIRouter
from .endpoints import user as UserRouter, posts as PostsRouter

Router = APIRouter()
Router.include_router(UserRouter.router, prefix="/users", tags=["users"])
# Router.include_router(PostsRouter.router, prefix="/posts", tags=["posts"])
