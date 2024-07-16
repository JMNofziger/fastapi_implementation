from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from os import environ
import logging


logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)
load_dotenv()

db_pass = environ.get("POSTGRESQL_DATABASE_PASSWORD")

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{db_pass}@localhost/fastapiFCC"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
logger.debug("Database connection was successful!")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
