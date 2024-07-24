from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
from dotenv import load_dotenv
from os import environ
from psycopg2.extras import RealDictCursor
import psycopg2
import logging
import time
import models
import schemas
import utils
from sqlalchemy.orm import Session
from database import engine, get_db

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


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    logger.debug("getting all posts")
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # relate input post to correct model columns
    new_post = models.Post(**post.model_dump())
    # create entry for database
    db.add(new_post)
    # push entry to database
    db.commit()
    # ask the database for the committed entry and store in 'new_post'
    db.refresh(new_post)
    logger.debug(new_post.__dict__.items())
    logger.debug(type(new_post))

    return new_post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # returned_post = db.query(models.Post).filter(models.Post.id == id).first()
    returned_post = db.query(models.Post).get(id)
    if not returned_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    return returned_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    index = db.query(models.Post).get(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )
    logger.debug(index.__dict__.items())
    db.delete(index)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # do i need to call for old post - no, I already have id
    # update the db post with the corresponding id
    # input post data must be structure for putting into the db

    post_query = db.query(models.Post).filter(models.Post.id == id)
    logger.debug(post_query)
    # get the first result of the query we assembled above
    post_to_update = post_query.first()

    if post_to_update == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    # check post value before update
    logger.debug(post_to_update.__dict__.items())
    # push post from model update to db to update existing post
    post_query.update(post.model_dump())
    # get latest value
    db.refresh(post_to_update)
    # show updated values in log
    logger.debug(post_to_update.__dict__.items())
    # commit change to db
    db.commit()
    # show updated values in log
    logger.debug(post_to_update)
    return post_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password from user input with bycrypt
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    logger.debug(id)
    user = db.query(models.User).filter(models.User.id == id).first()
    logger.debug(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not exist.",
        )
    return user
