from fastapi import FastAPI
from dotenv import load_dotenv
from os import environ
import logging
import models
from database import engine
from routers import post, user, auth

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)
load_dotenv()

# initialize/create all the defined models for tables
models.Base.metadata.create_all(bind=engine)
# initialize FastAPI app
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
