from enum import Enum
from sqlalchemy import Table, Column, Integer, String, DATETIME, ForeignKey, Interval, Geo
from datetime import datetime
from sqlalchemy.orm import relation, relationship
from sqlalchemy.sql.elements import Case
from sqlalchemy.sql.expression import column
from sqlalchemy.sql.sqltypes import DATE, Float
from .base import Base

class User(Base):
  id = Column(String, primary_key=True, index=True)
  name = Column(String, index=True)
  mail = Column(String, unique=True, index=True, nullable=False)
  password_hash = Column(String, nullable=False)
  avatar_url = Column(String, nullable=True)
  created_at = Column(DATETIME, default=datetime.now)
  updated_at = Column(DATETIME, default=datetime.now)
  date_of_birth = Column(DATETIME, index=True, nullable=True)

  posts = relationship('Post', backref='user')

class Post(Base):
  id = Column(String, primary_key=True, index=True)
  content = Column(String(500), nullable=False)
  content_length = Column(Integer, nullable=False)
  user_id = Column(String(), ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  reply_to_id = Column(String, ForeignKey('post.id', onupdate='CASCADE', ondelete='CASCADE', nullable=True))
  reply_to = relationship('Post', lazy='joined', join_depth=1)
  writing_time = Column(Interval, index=True, nullable=False)
  lat = Column(Float, index=True, nullable=True)
  lng = Column(Float, index=True, nullable=True)
  elevation = Column(Float, index=True, nullable=True)
  velocity = Column(Float, index=True, nullable=True)
  direction = Column(Float, index=True, nullable=True) # 0.0 - 360.0
  weather = Column(String(), index=True, nullable=True)
  gyro_x = Column(Float, index=True, nullable=True)
  gyro_y = Column(Float, index=True, nullable=True)
  gyro_z = Column(Float, index=True, nullable=True)
  created_at = Column(DATETIME, default=datetime.now)

  seen_users = relationship(
    'User',
    secondary='seen',
  )
  seen = relationship('Seen')

  favorited_users = relationship(
    'User',
    secondary='favorite',
  )
  seen = relationship('Favorite')

class Seen(Base):
  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  user_id = Column(String(), ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  post_id = Column(String(), ForeignKey('post.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  created_at = Column(DATETIME, default=datetime.now)

  user = relationship('User')
  post = relationship('Post')

class Favorite(Base):
  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  user_id = Column(String(), ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  post_id = Column(String(), ForeignKey('post.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  created_at = Column(DATETIME, default=datetime.now)
  updated_at = Column(DATETIME, default=datetime.now)

  user = relationship('User')
  post = relationship('Post')