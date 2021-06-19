from cruds.users.auth import get_current_user
from cruds.image import upload_image
from os import name
from routers import posts
from sqlalchemy.sql.elements import Null, and_, or_
from schemas.user import User
from schemas.post import BasePost, MaxMin, Post, QueryPost
from schemas.image import Image
from cruds.users import get_user_by_id
from typing import List, Optional, Set
from starlette.exceptions import HTTPException
from db import schemas as models
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import hashlib

def get_timeline(db: Session) -> List[Post]:
	posts = db.query(models.Post).all()
	return list(map(Post.from_orm, posts))

def get_query_timeline(db: Session, request: QueryPost, user: User) -> List[Post]:
	query_timeline = db.query(models.Post)
	if request.filter.temperture:
		if request.filter.temperture.max:
			query_timeline = query_timeline.filter(models.Post.tempurture < request.filter.temperture.max)
		if request.filter.temperture.min:
			query_timeline = query_timeline.filter(models.Post.tempurture >= request.filter.temperture.min)
	if request.filter.velocity:
		if request.filter.velocity.max:
			query_timeline = query_timeline.filter(models.Post.velocity < request.filter.velocity.max)
		if request.filter.velocity.min:
			query_timeline = query_timeline.filter(models.Post.velocity >= request.filter.velocity.min)
	if request.filter.elevation:
		if request.filter.elevation.max:
			query_timeline = query_timeline.filter(models.Post.elevation < request.filter.elevation.max)
		if request.filter.elevation.min:
			query_timeline = query_timeline.filter(models.Post.elevation >= request.filter.elevation.min)
	if request.filter.direction:
		if request.filter.direction == "up":
			query_timeline = query_timeline.filter(-30 < models.Post.gyro_x < 30, -30 < models.Post.gyro_y < 30)
		if request.filter.direction == "down":
			query_timeline = query_timeline.filter(or_(150 < models.Post.gyro_x, models.Post.gyro_x < -150), -30 < models.Post.gyro_y < 30)
	if request.sort.attr == "writing_time":
		query_timeline = query_timeline.order_by(models.Post.writing_time)
	if request.sort.attr == "velocity":
		query_timeline = query_timeline.order_by(models.Post.velocity)
	if request.sort.attr == "elevation":
		query_timeline = query_timeline.order_by(models.Post.elevation)

	query_timeline = list(map(Post.from_orm, query_timeline))

	if request.sort.attr == "birthday":
		user_date_of_birth = user.date_of_birth
		query_timeline = sorted(query_timeline, key=lambda x:abs(x.user.date_of_birth - user_date_of_birth))
	if request.sort.attr == "seen":
		query_timeline = sorted(query_timeline, key=lambda x:len(x.seen_users))


	if request.sort.order == "desc":
		query_timeline.reverse()

	return query_timeline

def create_post(db: Session, 
		token: str,
		content: str, 
		reply_to_id: Optional[str], 
		writing_time: timedelta, 
		lat: Optional[float], 
		lng: Optional[float], 
		elevation: Optional[float], 
		velocity: Optional[float], 
		direction: Optional[float], 
		tempurture: Optional[float], 
		weather: Optional[str], 
		gyro_x: Optional[float], 
		gyro_y: Optional[float], 
		gyro_z: Optional[float],
		images: Optional[List[Image]]
		) -> Post:
	if len(content) <= 0:
		raise HTTPException(400, 'The content is empty')

	if reply_to_id:
		if not get_post_by_id(db, reply_to_id):
			raise HTTPException(404, 'Post to reply not found')

	user = get_current_user(db, token)

	post_orm = models.Post(
		content=content,
		content_length=len(content),
		user_id=user.id,
		reply_to_id=reply_to_id,
		writing_time=writing_time,
		lat=lat,
		lng=lng,
		elevation=elevation,
		velocity=velocity,
		direction=direction,
		tempurture=tempurture,
		weather=weather,
		gyro_x=gyro_x,
		gyro_y=gyro_y,
		gyro_z=gyro_z,
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
