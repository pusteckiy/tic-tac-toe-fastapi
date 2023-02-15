import databases
from sqlalchemy import create_engine, MetaData

from src.config import settings


database = databases.Database(settings.DATABASE_URL)
metadata = MetaData()

engine = create_engine(
    settings.DATABASE_URL,
    # connect_args={"check_same_thread": False}
)
