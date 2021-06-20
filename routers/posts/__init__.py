from sqlalchemy.orm import query
from cruds.users.auth import get_current_user
from cruds.seen import seeing_post
from cruds.favorite import favoriting_post, unfavoriting_post
from cruds import posts
from cruds.posts import get_post_by_id, get_query_timeline, get_timeline, create_post
from sqlalchemy.sql.elements import Null
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from starlette.exceptions import HTTPException
from db import get_db
from schemas.post import Post, BasePost, CreatePost, QueryPost
from schemas.favorite import Favorite
from schemas.seen import Seen
from typing import List
from routers.users import oauth2_scheme

post_router = APIRouter()

@post_router.post('/', response_model=Post)
def post(payload: CreatePost, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
	post = create_post(
		db, 
		token,
		payload.content, 
		payload.reply_to_id, 
		payload.writing_time, 
		payload.lat, 
		payload.lng, 
		payload.elevation, 
		payload.velocity, 
		payload.direction,
		payload.gyro_x, 
		payload.gyro_y, 
		payload.gyro_z,
		payload.images
		)
	return post

@post_router.get('/', response_model=List[Post])
def timeline(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
	get_current_user(db, token)
	timeline = get_timeline(db)
	return timeline

@post_router.get('/search/{post_id}', response_model=Post)
def search_post(post_id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
	get_current_user(db, token)
	post = get_post_by_id(db, post_id)
	return post

@post_router.post('/query', response_model=List[Post])
def search_query_post(request: QueryPost, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
	user = get_current_user(db, token)
	query_timeline = get_query_timeline(db, request, user)
	return query_timeline

@post_router.put('/favorite/{post_id}', response_model=Favorite)
def favorite_post(post_id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
	get_current_user(db, token)
	favorite = favoriting_post(db, post_id, token)
	return favorite

@post_router.delete('/unfavorite/{post_id}', response_model=None)
def unfavorite_post(post_id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
	unfavoriting_post(db, post_id, token)
	return None

@post_router.put('/seen/{post_id}', response_model=Seen)
def see_post(post_id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
	seen = seeing_post(db, post_id, token)
	return seen