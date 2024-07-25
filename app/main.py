from fastapi import FastAPI
from dotenv import load_dotenv
from os import environ
from psycopg2.extras import RealDictCursor
import psycopg2
import logging
import time
import models
from database import engine, get_db
from routers import post, user, auth

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)
load_dotenv()

# initialize/create all the defined models for tables
models.Base.metadata.create_all(bind=engine)
# initialize FastAPI app
app = FastAPI()


# validate connection to database
while True:
    try:
        db_pass = environ.get("POSTGRESQL_DATABASE_PASSWORD")
        conn = psycopg2.connect(
            host="localhost",
            database="fastapiFCC",
            user="postgres",
            password=db_pass,
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        logger.debug("Database connection was successful!")
        break
    except Exception as err:
        logger.debug(f"attempted connection to db failed: {err}")
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
