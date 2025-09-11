from fastapi import FastAPI
from app.database import models
from app.database.database import engin
from app.routers import blog, user,login_auth ,refresh
from app.logging.logging_function import  logger
from fastapi import Request
import  time

fastapp = FastAPI(
    title='Blogs CRUD'
)        #Creating the instance of the fast API

models.Base.metadata.create_all(engin)  #Creating the database using the data connection URL


@fastapp.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    # logger.info(f"--> Request: {request.method} {request.url}")
    response = await call_next(request)
    # logger.info(f"<--Response: {response.status_code} for {request.method} {request.url}")

    process_time = (time.time() - start_time) * 1000
    logger.info(
        f"<-- Response: {response.status_code} for Request = {request.method} {request.url} "
        f"(completed in {process_time:.2f} ms)"
    )

    return response

fastapp.include_router(user.router)   #user router data
fastapp.include_router(login_auth.router)
fastapp.include_router(blog.router)
fastapp.include_router(refresh.refresh_router)



