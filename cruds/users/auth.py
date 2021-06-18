from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm.session import Session
from starlette.exceptions import HTTPException
from cruds.users import authenticate_user, get_user, get_user_by_id
from schemas.user import User
import jwt

SECRET = 'da3d19d89731b8773051a3eeeadcd854c4f2b1b08016c22c215cad34f78f6a62'
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	
	to_encode.update({
		'exp': expire
	})

	token = jwt.encode(to_encode, SECRET, algorithm='HS256')
	return token


def signin(db: Session, email: str, password: str) -> str:
	user = authenticate_user(db, email, password)
	token = create_access_token({
		'sub': user.id
	})

	return token

def get_current_user(db: Session, token: str) -> User:
	credentials_exception = HTTPException(
		401,
		detail='Could not validate credentials',
		headers={
			'WWW-Authenticate': 'Bearer'
		}
	)

	try:
		payload = jwt.decode(token, SECRET, algorithms=['HS256'])
		user_id: str = payload.get('sub')
		if user_id == None:
			raise credentials_exception
	except:
		raise credentials_exception
	
	user = get_user_by_id(db, user_id)
	if user == None:
		raise credentials_exception
	
	return user