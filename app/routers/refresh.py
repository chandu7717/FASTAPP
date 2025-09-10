from fastapi import APIRouter

from app.authentication import JWT_token
from app.schema import schemas

refresh_router = APIRouter(
    tags=["refresh Token"],
    prefix="/refresh"
)

@refresh_router.post('/')
def refresh_route_token(refresh: schemas.RefreshTokenRequest):
    payload = JWT_token.verify_refresh_token(refresh.refresh_token)
    user_id = payload.get('sub')

    new_access_token = JWT_token.create_access_token(data={"sub": user_id})

    return {
        "access_token": new_access_token,
        "token_type": 'bearer'
    }
