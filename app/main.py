from fastapi import FastAPI
from app.database import models
from app.database.database import engin
from app.routers import blog, user,login_auth ,refresh

fastapp = FastAPI()        #Creating the instance of the fast API

models.Base.metadata.create_all(engin)  #Creating the database using the data connection URL

fastapp.include_router(user.router)   #user router data
fastapp.include_router(login_auth.router)
fastapp.include_router(blog.router)
fastapp.include_router(refresh.refresh_router)



