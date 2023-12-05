from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
class Post(Base):
    __tablename__='mypost'
    
    id=Column(Integer, nullable=False, primary_key=True)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False)
    published=Column(Boolean, nullable=False, default=True, server_default='TRUE')
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                    nullable=False)
    owner=relationship("User")
    
    
    
class User(Base):
    __tablename__='users'
    id=Column(Integer, nullable=False, primary_key=True)
    email=Column(String, nullable=False, unique=True)
    password=Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
   
class Votes(Base):
    __tablename__="votes"
    user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
    post_id=Column(Integer, ForeignKey("mypost.id", ondelete="CASCADE"), primary_key=True)
    user=relationship("User")
    post=relationship("Post")