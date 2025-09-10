from typing import List
from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.authentication import oauth2
from app.schema import schemas
from app.database.database import get_db
from app.database import models
from app.service import blog_functions

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)


@router.get('/', response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(get_db), get_current_user: models.User = Depends(oauth2.get_current_user)):
    return blog_functions.get_all_blogs(db, get_current_user)


# Create blog
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.BlogBase,
                db: Session = Depends(get_db), current_user: models.User = Depends(
            oauth2.get_current_user)):  # Depends Means the dependency injection opens the DB Session

    return blog_functions.create_blogs(db, request, current_user)


# Gat the blog based on the blog id
@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def get_blog(request_id, db: Session = Depends(get_db),
             get_current_user: models.User = Depends(oauth2.get_current_user)):
    return blog_functions.get_blog_on_id(db, request_id, get_current_user)


# #Update blog
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.BlogBase, db: Session = Depends(get_db),
                get_current_user: models.User = Depends(oauth2.get_current_user)):
    return blog_functions.update_blog_id(id, db, request, get_current_user)


# Delete  = deleting blog

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db), get_current_user: models.User = Depends(oauth2.get_current_user)):
    return blog_functions.delete_blog_id(id, db, get_current_user)
