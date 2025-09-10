from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.database import models
from app.schema import schemas


def get_all_blogs(db: Session, current_user: models.User):
    return db.query(models.Blog).filter(models.Blog.user_id == current_user.id).all()


# Create blog
def create_blogs(db: Session, request: schemas.BlogBase, current_user: models.User):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


# get the blog based on the blog id
def get_blog_on_id(db: Session, request_id: int, current_user: models.User):
    blogs = db.query(models.Blog).filter(models.Blog.id == request_id).first()
    if not blogs:
        # response.status_code = status.HTTP_404_NOT_FOUND
        #
        # return {
        #     "Details": f"Blog with the {request_id} is not found in the DB"
        # }

        raise HTTPException(status_code=404, detail=f'The blog {request_id} not found in the data base')

    if blogs.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"this blog with id={request_id} is not associated with this user")
    return blogs


# Updating the blog with the id
def update_blog_id(id: int, db: Session, request: schemas.BlogBase, current_user: models.User):
    blog_querry = db.query(models.Blog).filter(models.Blog.id == id)
    blog = blog_querry.first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id={id} blog is not found in DB")

    if blog.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorized to update this blog")

    blog_querry.update(request.dict())

    db.commit()
    db.refresh(blog)

    return {
        "Message": f"{id} blog is updated successfully"
    }


# deleting the blog

def delete_blog_id(id: int, db: Session, current_user: models.User):
    del_querry = db.query(models.Blog).filter(models.Blog.id == id)
    del_blog = del_querry.first()
    if not del_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id} this blog is not exist in the data base")

    if del_blog.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorized to delete this blog")

    del_querry.delete(synchronize_session=False)
    db.commit()
    return {
        "status": "done"
    }
