from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from app.schema import schemas
from app.database.database import get_db
from app.service import user_functions


router = APIRouter(
    prefix='/user',
    tags=['Users']
)


# Creating the user dataa
@router.post("/", response_model=schemas.ShowUser , status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.Users, db: Session = Depends(get_db)):
    return user_functions.create_user(db, request)


# Get all the user data
@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_functions.get_user_data(user_id, db)
