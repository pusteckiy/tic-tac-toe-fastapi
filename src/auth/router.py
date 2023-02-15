from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.services import auth_user, get_user_by_token
from src.auth.schemas import User


router = APIRouter(
    prefix='/account',
    tags=['Account']
)


@router.post('/auth')
async def create_or_login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = await auth_user(form_data.username, form_data.password)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/me')
async def get_user(user: User = Depends(get_user_by_token)) -> User:
    return user
