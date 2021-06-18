from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from cruds.users.auth import get_current_user, signin
from schemas.user import BaseUser, Token, User
from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from starlette.exceptions import HTTPException
from db import get_db
from cruds.users import create_user, get_user, get_user_by_id
from schemas.user import User

user_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/users/token')

@user_router.post('/signup', response_model=User)
def signup(payload: BaseUser, db: Session = Depends(get_db)):
	user = create_user(db, payload.username, payload.email, payload.date_of_birth, payload.password, payload.avatar_url)
	return user

@user_router.post('/token', response_model=Token)
def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	t = signin(db, form_data.username, form_data.password)
	return Token(access_token=t, token_type='Bearer')

@user_router.get('/me', response_model=User)
def me(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
	user = get_current_user(db, token)
	return user

@user_router.get('/search/{user_id}', response_model=User)
def search_user(user_id: str, db: Session = Depends(get_db)):
	user = get_user_by_id(db, user_id)
	return user