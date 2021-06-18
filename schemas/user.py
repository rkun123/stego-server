from typing import List, Optional
from datetime import date, datetime, timedelta
from pydantic import BaseModel, Field, validator
import re

class BaseUser(BaseModel):
	username: str = Field()
	email: str = Field()
	password: Optional[str] = Field()
	password_hash: Optional[str] = Field()
	avatar_url: Optional[str] = Field()
	date_of_birth: Optional[datetime] = Field()

	class Config:
		orm_mode = True
	
	@validator('email')
	def email_format(cls, v):
		assert re.fullmatch(r'^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$', v), 'email must be valid format'
		return v

class User(BaseUser):
	id: str = Field()
	created_at: datetime = Field(default_factory=datetime.now)
	updated_at: datetime = Field(default_factory=datetime.now)

	class Config:
		orm_mode = True

class Token(BaseModel):
	access_token: str = Field()
	token_type: str = Field()

class GetAccessToken(BaseModel):
	email: str = Field()
	password: str = Field()