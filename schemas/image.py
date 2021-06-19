from pydantic import BaseModel, Field
from datetime import datetime

class BaseImage(BaseModel):
	image_url: str
	post_id: str

	class Config:
		orm_mode = True

class Image(BaseImage):
	id: str = Field()
	created_at: datetime = Field(default_factory=datetime.now)
	updated_at: datetime = Field(default_factory=datetime.now)