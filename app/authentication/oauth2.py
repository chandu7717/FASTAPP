from fastapi import Depends ,HTTPException ,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.authentication import JWT_token
from app.database import models
from app.database import database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  #From login route the fast api fetch the token

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = JWT_token.verify_token(token, credentials_exception)  #here we got the current user email after decoding the access token
   #TokenData(email="alice@example.com")
    user = db.query(models.User).filter(models.User.id == int(token_data.userID)).first()

    if not user:
        raise credentials_exception
    return  user   #We are getting the current user table data like id,name,email





