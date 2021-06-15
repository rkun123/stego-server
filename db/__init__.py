from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///./main.db')
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)