import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

current_file_path = os.path.abspath(__file__)
database_directory = os.path.dirname(current_file_path)

SQLALCHEMY_DATABASE_URL = f'sqlite:///{database_directory}/locations.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
