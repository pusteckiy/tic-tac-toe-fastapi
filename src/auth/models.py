from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from src.db.core import metadata


users = Table(
    "users",
    metadata,

    Column("id", Integer, primary_key=True),
    Column("username", String(32), unique=True),
    Column("password", String(64)),
    Column("games_all", Integer, server_default='0'),
    Column("games_won", Integer, server_default='0'),
    Column("connected_game", ForeignKey('games.id')),
    Column("created_at", DateTime, server_default=func.now())
)