from fastapi import APIRouter
from .endpoints import user as UserRouter
from .endpoints import followings as FollowingsRouter
from .endpoints import posts as PostsRouter
from .endpoints import likes as LikesRouter
from .endpoints import comments as CommentsRouter

Router = APIRouter()
Router.include_router(UserRouter.router, prefix="/users", tags=["Users"])
Router.include_router(FollowingsRouter.router, prefix="/user", tags=["Users"])
Router.include_router(PostsRouter.router, prefix="/posts", tags=["Posts"])
Router.include_router(LikesRouter.router, prefix="/post/like", tags=["Posts"])
Router.include_router(CommentsRouter.router, prefix="/post/comments", tags=["Posts"])
