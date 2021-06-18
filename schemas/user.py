from typing import List, Optional
from datetime import date, datetime, timedelta
from pydantic import BaseModel, Field


class CreateUser(BaseModel):
	username: str = Field()
	email: str = Field()
	password: str = Field()
	avatar_url: Optional[str] = Field()
	date_of_birth: Optional[datetime] = Field()

	class Config:
		orm_mode = True

class BaseUser(BaseModel):
	username: str = Field()
	email: str = Field()
	password_hash: str = Field()
	avatar_url: Optional[str] = Field()
	date_of_birth: Optional[datetime] = Field()

	class Config:
		orm_mode = True

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