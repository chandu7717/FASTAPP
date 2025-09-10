from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from app.authentication import hashing
from app.schema import schemas
from app.database import models


#Creating the user
def create_user(db: Session, request: schemas.Users):
    new_user = models.User(name=request.name, email=request.email,
                           password=hashing.HashPassword.bcrypt_pwd(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#get the user data
def get_user_data(id:int,db:Session):
    user_data = db.query(models.User).filter(models.User.id == id).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id={id} user is not found in the db")
    return user_data

