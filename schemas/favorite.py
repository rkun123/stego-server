from pydantic import BaseModel, Field
from datetime import datetime

class BaseFavorite(BaseModel):
	user_id: str
	post_id: str

	class Config:
		orm_mode = True

class Favorite(BaseFavorite):
	id: int = Field()
	created_at: datetime = Field(default_factory=datetime.now)
	updated_at: datetime = Field(default_factory=datetime.now)