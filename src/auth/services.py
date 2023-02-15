import bcrypt
import jwt

from datetime  import timedelta, datetime
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from src.config import settings
from src.auth.models import users
from src.db.core import database


async def auth_user(username: str, password: str) -> str:
    query = users.select().where(users.columns.username == username)
    result = await database.fetch_one(query)
    if result:
        user_id = result[0]
    else:
        hashed_password = hash_password(password)
        query = users.insert().values(username=username, password=hashed_password)
        user_id = await database.execute(query)
    return create_token({'user_id': user_id})


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=10)
    return str(bcrypt.hashpw(password.encode('utf-8'), salt))


def verify_password(plain_password: str, hash_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hash_password)


def create_token(data: dict, expires_delta: int = settings.JWT_EXPIRES_SEC):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(payload=to_encode, key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="account/auth")
async def get_user_by_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except jwt.DecodeError:
        return HTTPException(status_code=401, detail='error while JWT decoding')
    except jwt.ExpiredSignatureError:
        return HTTPException(status_code=401, detail='token has expired')
    user_id = payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=401, detail='could not validate credentials')
    query = users.select().where(users.columns.id == user_id)
    return await database.fetch_one(query)


async def increment_win(user: dict):
    query = users.update().where(users.columns.id==user.id).values(games_won=user.games_won + 1)
    await database.execute(query)
