from .image import Image
from typing import List, Optional, Union
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, validator
from .user import BaseUser, User
import re

class BasePost(BaseModel):
	content: str = Field()
	content_length: int = Field()
	user_id: str = Field()
	reply_to_id: Optional[str] = Field()
	writing_time: timedelta = Field()
	lat: Optional[float] = Field()
	lng: Optional[float] = Field()
	elevation: Optional[float] = Field()
	velocity: Optional[float] = Field()
	direction: Optional[float] = Field()
	tempurture: Optional[float] = Field()
	weather: Optional[str] = Field()
	gyro_x: Optional[float] = Field()
	gyro_y: Optional[float] = Field()
	gyro_z: Optional[float] = Field()
	
	user: User = Field()
	
	seen_users: List[Union[User, BaseUser]] = Field()
	favorited_users: List[Union[User, BaseUser]] = Field()
	images: Optional[List[Image]] = Field()

	class Config:
		orm_mode = True

class Post(BasePost):
	id: str = Field()
	created_at: datetime = Field(default_factory=datetime.now)
	updated_at: datetime = Field(default_factory=datetime.now)

class CreatePost(BaseModel):
	content: str = Field()
	reply_to_id: Optional[str] = Field()
	writing_time: timedelta = Field()
	lat: Optional[float] = Field()
	lng: Optional[float] = Field()
	elevation: Optional[float] = Field()
	velocity: Optional[float] = Field()
	tempurture: Optional[float] = Field()
	direction: Optional[float] = Field()
	weather: Optional[str] = Field()
	gyro_x: Optional[float] = Field()
	gyro_y: Optional[float] = Field()
	gyro_z: Optional[float] = Field()

	images: List[Image] = Field()

	class Config:
		orm_mode = True

class Sort(BaseModel):
	attr: str = Field()
	order: str = Field()

	@validator('attr')
	def attr_format(cls, v):
		assert re.fullmatch(r'writing_time|birthday|seen|velocity|elevation|position', v), 'attribute must be valid format'
		return v
	@validator('order')
	def order_format(cls, v):
		assert re.fullmatch(r'asc|desc', v), 'order must be valid format'
		return v

class MaxMin(BaseModel):
	max: Optional[float] = Field()
	min: Optional[float] = Field()

class Filter(BaseModel):
	temperture: Optional[MaxMin] = Field()
	velocity: Optional[MaxMin] = Field()
	direction: Optional[str] = Field()
	elevation: Optional[MaxMin] = Field()

	@validator('direction')
	def direction_format(cls, v):
		assert re.fullmatch(r'up|down', v), 'direction must be valid format'
		return v

class QueryPost(BaseModel):
	sort: Optional[Sort] = Field()
	filter: Optional[Filter] = Field()

	class Config:
		orm_mode = True
	