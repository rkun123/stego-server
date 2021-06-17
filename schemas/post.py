from typing import List, String, Optional, Union
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from .user import BaseUser, User

class BasePost(BaseModel):
	content: String = Field()
	content_length: float = Field()
	user_id: String = Field()
	reply_to_id: Optional[String] = Field()
	writing_time: timedelta = Field()
	lat: Optional[float] = Field()
	lng: Optional[float] = Field()
	elevation: Optional[float] = Field()
	velocity: Optional[float] = Field()
	direction: Optional[float] = Field()
	weathre: Optional[String] = Field()
	gyro_x: Optional[float] = Field()
	gyro_y: Optional[float] = Field()
	gyro_z: Optional[float] = Field()

	seen_users: List[Union[User, BaseUser]] = Field()
	favorited_users: List[Union[User, BaseUser]] = Field()

	class Config:
		orm_mode = True

class Post(BasePost):
	id: String = Field()
	created_at: datetime = Field(default_factory=datetime.now)
	updated_at: datetime = Field(default_factory=datetime.now)