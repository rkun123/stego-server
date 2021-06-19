from pydantic import BaseModel, Field
from datetime import datetime

class BaseSeen(BaseModel):
	user_id: str
	post_id: str

	class Config:
		orm_mode = True

class Seen(BaseSeen):
	id: str = Field()
	created_at: datetime = Field(default_factory=datetime.now)
	updated_at: datetime = Field(default_factory=datetime.now)