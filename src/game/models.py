from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func

from src.db.core import metadata


games = Table(
    "games",
    metadata,

    Column("id", Integer, primary_key=True),
    Column("code", String, unique=True),
    Column("end", Boolean, server_default="false"),
    Column("next", ForeignKey("users.id")),
    Column("winner", ForeignKey("users.id")),
    Column("created_at", DateTime, server_default=func.now())
)


cells = Table(
    "cells",
    metadata,

    Column("game", ForeignKey("games.id", ondelete="CASCADE"), primary_key=True),
    Column("x", Integer, primary_key=True, nullable=False),
    Column("y", Integer, primary_key=True, nullable=False),
    Column("z", Integer, primary_key=True, nullable=False),
    Column("player", String, nullable=False)
)