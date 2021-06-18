from cruds.users.auth import signin
from schemas.user import CreateUser, GetAccessToken, Token, User
from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from starlette.exceptions import HTTPException
from db import get_db
from cruds.users import create_user, get_user
from schemas.user import User

user_router = APIRouter()

@user_router.post('/signup', response_model=User)
def signup(payload: CreateUser, db: Session = Depends(get_db)):
	user = create_user(db, payload.username, payload.email, payload.date_of_birth, payload.password, payload.avatar_url)
	return user

@user_router.post('/token', response_model=Token)
def token(payload: GetAccessToken, db: Session = Depends(get_db)):
	t = signin(db, payload.email, payload.password)
	return Token(access_token=t, token_type='Bearer')