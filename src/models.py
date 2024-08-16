import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    UserId = Column(Integer, primary_key=True)
    Username = Column(String(32), nullable=False, unique=True) 
    FirstName = Column(String(250), nullable=True)
    LastName = Column(String(250), nullable=True)
    Email = Column(String(250), nullable=True, unique=True)


class Post(Base):
    __tablename__ = 'post'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    PostID = Column(Integer, primary_key=True)
    User_ID = Column(Integer, ForeignKey('user.UserId'), nullable=False)  
    user = relationship('User', back_populates='posts')  
    media = relationship('Media', back_populates='post')
    comments = relationship('Comment', back_populates='post')

class Media(Base):
    __tablename__ = 'media'
    MediaID = Column(Integer, primary_key=True)
    Type = Column(Enum('image', 'video'), nullable=False)
    URL = Column(String(250), nullable=False)
    Post_ID = Column(Integer, ForeignKey('post.PostID'), nullable=False)
    Post = relationship("Post", back_populates="media")

class Comment(Base):
    __tablename__ = 'comment'
    CommentId = Column(Integer, primary_key=True, autoincrement=True)
    Comment_text = Column(String, nullable=False)
    AuthorId = Column(Integer, ForeignKey('user.UserID'), nullable=False)
    PostId = Column(Integer, ForeignKey('post.PostID'), nullable=False)
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class Follower(Base):
    __tablename__ = 'follower'
    User_From_ID = Column(Integer, ForeignKey('user.UserID'), primary_key=True)
    User_To_ID = Column(Integer, ForeignKey('user.UserID'), primary_key=True)

    follower = relationship("User", foreign_keys=[User_From_ID])
    followed = relationship("User", foreign_keys=[User_To_ID])

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
