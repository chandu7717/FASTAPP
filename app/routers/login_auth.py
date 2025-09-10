from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.authentication import JWT_token
from app.authentication.hashing import HashPassword
from app.database import models
from app.database.database import get_db
from app.schema import schemas

router = APIRouter(
    tags=['Login Authentication']
)


@router.post('/login')
def user_auth(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    check_user = db.query(models.User).filter(models.User.email == request.username).first()
    if not check_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid credentials")

    if not HashPassword.verify(check_user.password,
                               request.password):  # Comparing with the hashed pwd in the db with the request password
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password')

    # generate JWT Access token
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWT_token.create_access_token(data={"sub": str(check_user.id)})
    refresh_token = JWT_token.create_refresh_token(data={"sub": str(check_user.id)})

    return schemas.Token(access_token=access_token,
                         refresh_token=refresh_token,
                         token_type="bearer")
