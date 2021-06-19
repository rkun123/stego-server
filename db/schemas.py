from enum import Enum
from sqlalchemy.schema import Sequence
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Interval
from datetime import datetime
from sqlalchemy.orm import relation, relationship
from sqlalchemy.sql.elements import Case
from sqlalchemy.sql.expression import column
from sqlalchemy.sql.sqltypes import DATE, Float
from utils.gen_primarykey import gen_primarykey
from .base import Base

class User(Base):
  id = Column(String, default=gen_primarykey, primary_key=True, index=True)
  username = Column(String, unique=True, index=True)
  email = Column(String, unique=True, index=True, nullable=False)
  password_hash = Column(String, nullable=False)
  avatar_url = Column(String, nullable=True)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)
  date_of_birth = Column(DateTime, index=True, nullable=True)

  posts = relationship('Post', back_populates='user')

class Post(Base):
  id = Column(String, default=gen_primarykey, primary_key=True, index=True)
  content = Column(String(500), nullable=False)
  content_length = Column(Integer, nullable=False)
  user_id = Column(String(), ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  reply_to_id = Column(String, ForeignKey('post.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
  reply_to = relationship('Post', lazy='joined', join_depth=1)
  writing_time = Column(Interval, index=True, nullable=False)
  lat = Column(Float, index=True, nullable=True)
  lng = Column(Float, index=True, nullable=True)
  elevation = Column(Float, index=True, nullable=True)
  velocity = Column(Float, index=True, nullable=True)
  direction = Column(Float, index=True, nullable=True) # 0.0 - 360.0
  tempurture = Column(Float, index=True, nullable=True)
  weather = Column(String(), index=True, nullable=True)
  gyro_x = Column(Float, index=True, nullable=True)
  gyro_y = Column(Float, index=True, nullable=True)
  gyro_z = Column(Float, index=True, nullable=True)
  created_at = Column(DateTime, default=datetime.now)

  user = relationship(
    'User',
  )

  images = relationship(
    'Image',
  )

  seen_users = relationship(
    'User',
    secondary='seen',
  )

  favorited_users = relationship(
    'User',
    secondary='favorite',
  )

class Seen(Base):
  id = Column(Integer, Sequence('id_seq', start=1, increment=1), primary_key=True)
  user_id = Column(String(), ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  post_id = Column(String(), ForeignKey('post.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  created_at = Column(DateTime, default=datetime.now)

class Favorite(Base):
  id = Column(Integer, Sequence('id_seq', start=1, increment=1), primary_key=True)
  user_id = Column(String(), ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  post_id = Column(String(), ForeignKey('post.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)

class Image(Base):
  id = Column(String, default=gen_primarykey, primary_key=True, index=True)
  image_url = Column(String)
  post_id = Column(String(), ForeignKey('post.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  created_at = Column(DateTime, default=datetime.now)
