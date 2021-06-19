from .image import Image
from typing import List, Optional, Union
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from .user import BaseUser, User

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
	weather: Optional[str] = Field()
	gyro_x: Optional[float] = Field()
	gyro_y: Optional[float] = Field()
	gyro_z: Optional[float] = Field()

	seen_users: List[Union[User, BaseUser]] = Field()
	favorited_users: List[Union[User, BaseUser]] = Field()
	images: List[Image] = Field()

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
	direction: Optional[float] = Field()
	weather: Optional[str] = Field()
	gyro_x: Optional[float] = Field()
	gyro_y: Optional[float] = Field()
	gyro_z: Optional[float] = Field()

	images: List[Image] = Field()

	class Config:
		orm_mode = True