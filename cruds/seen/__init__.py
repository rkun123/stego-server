from cruds.users.auth import get_current_user
from schemas.seen import Seen
from cruds.users import get_user_by_id
from cruds.posts import get_post_by_id
from sqlalchemy.orm import Session
from db import schemas as models
from starlette.exceptions import HTTPException

def seeing_post(db: Session, post_id: str, token: str) -> Seen:
	if get_post_by_id(db, post_id) == None:
		raise HTTPException(400, 'No such post')
	user = get_current_user(db, token)
	if db.query(models.Seen).filter(models.Seen.post_id == post_id, models.Seen.user_id == user.id).count():
		raise HTTPException(400, 'Already favorite the post')

	favorite_orm = models.Seen(user_id=user.id, post_id=post_id)
	
	db.add(favorite_orm)
	db.commit()
	db.refresh(favorite_orm)

	return Seen.from_orm(favorite_orm)
