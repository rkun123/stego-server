from fastapi import APIRouter
from .users import user_router
from .posts import post_router

r = APIRouter()
r.include_router(user_router, prefix='/users', tags=['users'])
r.include_router(post_router, prefix='/posts', tags=['posts'])