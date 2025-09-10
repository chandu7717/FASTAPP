from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class Blog(Base):                   #Any class that inherits from Base becomes a table definition.
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="blogs")


class User(Base):
    __tablename__ = 'users'     #users table

    id = Column(Integer, primary_key=True, index=True )   #Make this column as unique=True
    name = Column(String)
    email = Column(String)                               #Make this column as unique=True to donot allow the duplicate emails
    password = Column(String)

    blogs = relationship('Blog', back_populates="creator")