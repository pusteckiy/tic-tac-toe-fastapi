from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    username: str
    games_all: int = 0
    games_won: int = 0
