from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRESQL_DATABASE_URL = 'postgresql+psycopg2://postgres:Chandu%407717@localhost:5432/blog_DB'

engin  = create_engine(POSTGRESQL_DATABASE_URL)     #Create the connection and Create the Data base

SessionLocal = sessionmaker(bind=engin , autocommit=False,autoflush=False)
# sessionmaker is a factory function in SQLAlchemy.
# It creates a class that can generate new Session objects (DB connections).
# Think of it like a "session factory" → each time you call SessionLocal(), you get a new session connected to your database.

Base = declarative_base()

#Functionality of the Base Class

# #It’s a special parent class that gives any child class (like Blog) the ability to:
# Register itself as a table (__tablename__).
# Define columns (Column, Integer, String, etc.).
# Link Python classes ↔ Database tables (ORM mapping).


def get_db():  # Defines a dependency that creates a new DB session per request.
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
