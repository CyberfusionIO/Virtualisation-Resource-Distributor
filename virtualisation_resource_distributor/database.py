"""Database helpers."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from virtualisation_resource_distributor.config import settings

engine = create_engine(
    f"sqlite:///{settings.DATABASE_PATH}", pool_pre_ping=True
)

DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
