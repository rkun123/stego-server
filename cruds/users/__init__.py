from os import name
from typing import Optional
from starlette.exceptions import HTTPException
from schemas.user import BaseUser, User
from db import schemas as models
from sqlalchemy.orm import Session
from datetime import datetime
import hashlib


def hash_password(password: str) -> str:
	encoded = password.encode()
	hash = hashlib.sha256(encoded)
	return hash.hexdigest()

def create_user(db: Session, username: str, email: str, date_of_birth: datetime, password: str, avatar_url: str = None) -> User:
	hashed_password = hash_password(password)

	user = _get_user(db, email)
	if user != None:
		raise HTTPException(400, 'Specified email has already taken')
	
	user_orm = models.User(
		username=username,
		email=email,
		date_of_birth=date_of_birth,
		avatar_url=avatar_url,
		password_hash=hashed_password
	)

	db.add(user_orm)
	db.commit()
	db.refresh(user_orm)
	user = User.from_orm(user_orm)
	return user

def _get_user(db: Session, username: str) -> User:
	user_orm = db.query(models.User).filter(models.User.username == username).first()
	if user_orm == None:
		return None
	return User.from_orm(user_orm)


def get_user(db: Session, username: str) -> User:
	user = _get_user(db, username)
	if user == None:
		raise HTTPException(404, 'User not found')
	return user

def get_user_by_id(db: Session, id: str) -> Optional[User]:
	user_orm = db.query(models.User).get(id)
	if user_orm == None:
		return None
	return User.from_orm(user_orm)

def authenticate_user(db: Session, username: str, password: str) -> User:
	hashed_password = hash_password(password)
	user = get_user(db, username)
	if user.password_hash != hashed_password:
		raise HTTPException(401, 'password does not match')
	return user