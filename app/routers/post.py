from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from database import get_db
import schemas, models
import logging

# all method paths in this file begin with the prefix "posts"
router = APIRouter(prefix="/posts", tags=["Posts"])
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    logger.debug("getting all posts")
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
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


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # returned_post = db.query(models.Post).filter(models.Post.id == id).first()
    returned_post = db.query(models.Post).get(id)
    if not returned_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    return returned_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/{id}", response_model=schemas.Post)
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
