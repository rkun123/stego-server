import re
from sqlalchemy.sql.expression import desc
from cruds.users.auth import get_current_user
from cruds.image import upload_image
from sqlalchemy.sql.elements import or_
from schemas.user import User
from schemas.post import BasePost, MaxMin, Post, QueryPost
from schemas.image import Image
from typing import List, Optional, Set
from starlette.exceptions import HTTPException
from db import base, schemas as models
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
import requests

weather_api_key = os.environ.get('WEATHER_API_KEY')
base_url = "http://api.openweathermap.org/data/2.5/forecast"

def get_timeline(db: Session) -> List[Post]:
	posts = db.query(models.Post).order_by(desc(models.Post.created_at)).all()
	return list(map(Post.from_orm, posts))

def get_query_timeline(db: Session, request: QueryPost, user: User) -> List[Post]:
	query_timeline = db.query(models.Post)
	if request.filter:
		if request.filter.temperture:
			query_timeline = query_timeline.filter(models.Post.tempurture != None)
			if request.filter.temperture.max:
				query_timeline = query_timeline.filter(models.Post.tempurture < request.filter.temperture.max)
			if request.filter.temperture.min:
				query_timeline = query_timeline.filter(models.Post.tempurture >= request.filter.temperture.min)
		if request.filter.velocity:
			query_timeline = query_timeline.filter(models.Post.velocity != None)
			if request.filter.velocity.max:
				query_timeline = query_timeline.filter(models.Post.velocity < request.filter.velocity.max)
			if request.filter.velocity.min:
				query_timeline = query_timeline.filter(models.Post.velocity >= request.filter.velocity.min)
		if request.filter.elevation:
			query_timeline = query_timeline.filter(models.Post.elevation != None)
			if request.filter.elevation.max:
				query_timeline = query_timeline.filter(models.Post.elevation < request.filter.elevation.max)
			if request.filter.elevation.min:
				query_timeline = query_timeline.filter(models.Post.elevation >= request.filter.elevation.min)
		if request.filter.direction:
			query_timeline = query_timeline.filter(models.Post.gyro_x != None).filter(models.Post.gyro_y != None).filter(models.Post.gyro_z != None)
			if request.filter.direction == "up":
				query_timeline = query_timeline.filter(-30 < models.Post.gyro_x, models.Post.gyro_x < 30, -30 < models.Post.gyro_y, models.Post.gyro_y < 30)
			if request.filter.direction == "down":
				query_timeline = query_timeline.filter(or_(150 < models.Post.gyro_x, models.Post.gyro_x < -150)).filter(-30 < models.Post.gyro_y, models.Post.gyro_y < 30)
	if request.sort:
		if request.sort.attr == "writing_time":
			query_timeline = query_timeline.filter(models.Post.writing_time != None)
			query_timeline = query_timeline.order_by(models.Post.writing_time)
		if request.sort.attr == "velocity":
			query_timeline = query_timeline.filter(models.Post.velocity != None)
			query_timeline = query_timeline.order_by(models.Post.velocity)
		if request.sort.attr == "elevation":
			query_timeline = query_timeline.filter(models.Post.elevation != None)
			query_timeline = query_timeline.order_by(models.Post.elevation)
	else:
		query_timeline = query_timeline.order_by(desc(models.Post.created_at))
	
	query_timeline = query_timeline.all()

	query_timeline = list(map(Post.from_orm, query_timeline))

	if request.sort:
		if request.sort.attr == "birthday":
			query_timeline = list(filter(lambda x: x.user.date_of_birth != None, query_timeline))
			query_timeline = sorted(query_timeline, key=lambda x:x.user.date_of_birth)
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


	weather = None
	tempurture = None
	if lat != None and lng != None:
		res = requests.get(base_url + f"?lat={lat}&lon={lng}&APPID={weather_api_key}")
		res_json = res.json()
		print(res_json)
		if res_json['cod'] == '200':
			weather = res_json['list'][0]['weather'][0]['main']
			tempurture = res_json['list'][0]['main']['temp'] - 273.15

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
