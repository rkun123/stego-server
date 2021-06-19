from db import schemas as models
from sqlalchemy.sql.base import NO_ARG
from schemas.image import Image
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

def upload_image(db: Session, image_url: str, post_id: str) -> Image:
	image_orm = models.Image(image_url=image_url, post_id=post_id)

	db.add(image_orm)
	db.commit()
	db.refresh(image_orm)

	return Image.from_orm(image_orm)