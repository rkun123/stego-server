from cruds.image import upload_image
from os import name
from routers import posts
from sqlalchemy.sql.elements import Null
from schemas.post import BasePost, Post
from schemas.image import Image
from cruds.users import get_user_by_id
from typing import List, Optional, Set
from starlette.exceptions import HTTPException
from db import schemas as models
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import hashlib

def get_timeline(db: Session) -> List[Post]:
	return db.query(models.Post).all()

def create_post(db: Session, 
		content: str, 
		content_length: int, 
		user_id: str, 
		reply_to_id: Optional[str], 
		writing_time: timedelta, 
		lat: Optional[float], 
		lng: Optional[float], 
		elevation: Optional[float], 
		velocity: Optional[float], 
		direction: Optional[float], 
		weather: Optional[str], 
		gyro_x: Optional[float], 
		gyro_y: Optional[float], 
		gyro_z: Optional[float],
		images: Optional[List[Image]]
		) -> Post:
	if len(content) <= 0 or content_length <= 0:
		raise HTTPException(400, 'The content is empty')

	if not get_user_by_id(db, user_id):
		raise HTTPException(404, 'User not found')
	
	if reply_to_id:
		if not get_post_by_id(db, reply_to_id):
			raise HTTPException(404, 'Post not found')


	post_orm = models.Post(
		content=content,
		content_length=content_length,
		user_id=user_id,
		reply_to_id=reply_to_id,
		writing_time=writing_time,
		lat=lat,
		lng=lng,
		elevation=elevation,
		velocity=velocity,
		direction=direction,
		weather=weather,
		gyro_x=gyro_x,
		gyro_y=gyro_y,
		gyro_z=gyro_z,
		seen_users=[],
		favorited_users=[],
		images=[]
	)

	db.add(post_orm)
	db.commit()
	db.refresh(post_orm)
	for image in images:
		upload_image(db, image.image_url, post_orm.id)
	post = Post.from_orm(post_orm)
	return post

def get_post_by_id(db: Session, post_id: str) -> Post:
	post_orm = db.query(models.Post).get(post_id)
	if post_orm == None:
		return None
	return Post.from_orm(post_orm)
