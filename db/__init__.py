from sqlalchemy import create_engine
from starlette.exceptions import HTTPException
from sqlalchemy.orm import session, sessionmaker, Session
from .base import Base
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///./main.db')
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()