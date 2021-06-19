from cruds.users.auth import get_current_user
from sqlalchemy.sql.functions import user
from cruds.users import get_user_by_id
from cruds.posts import get_post_by_id
from schemas.favorite import Favorite
from sqlalchemy.orm import Session
from db import schemas as models
from starlette.exceptions import HTTPException

def favoriting_post(db: Session, post_id: str, token: str) -> Favorite:
	if get_post_by_id(db, post_id) == None:
		raise HTTPException(404, 'Post not found')
	user = get_current_user(db, token)
	if db.query(models.Favorite).filter(models.Favorite.post_id == post_id, models.Favorite.user_id == user.id).count():
		raise HTTPException(400, 'Already favorite the post')

	favorite_orm = models.Favorite(user_id=user.id, post_id=post_id)
	
	db.add(favorite_orm)
	db.commit()
	db.refresh(favorite_orm)

	return Favorite.from_orm(favorite_orm)

def unfavoriting_post(db: Session, post_id: str, token: str) -> None:
	if get_post_by_id(db, post_id) == None:
		raise HTTPException(404, 'Post not found')
	user = get_current_user(db, token)
	favorite_info = db.query(models.Favorite).filter(models.Favorite.post_id == post_id, models.Favorite.user_id == user.id).first()
	if favorite_info == None:
		raise HTTPException(400, 'You don\'t favorite the post')
	db.delete(favorite_info)
	db.commit()

	return None