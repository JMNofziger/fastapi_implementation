from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from database import get_db
from oauth2 import get_current_user
import schemas, models
from config import logger

# all method paths in this file begin with the prefix "posts"
router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db),
    # current_user: int = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = "",
):
    # filter to only return posts which are owned by the requestor
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    # relate input post to correct model columns - add owner_id to post object
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    # create entry for database
    db.add(new_post)
    # push entry to database
    db.commit()
    # ask the database for the committed entry and store in 'new_post'
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    returned_post = db.query(models.Post).get(id)
    if not returned_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    return returned_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    index = db.query(models.Post).get(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )
    elif index.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"You are not authorized to delete post {id}",
        )
    db.delete(index)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
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
    elif post_to_update.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"You are not authorized to modify post {id}",
        )
    # check post value before update
    logger.debug(post_to_update.__dict__.items())
    # push post from model update to db to update existing post
    post_query.update(post.model_dump())
    # get latest value
    db.refresh(post_to_update)
    db.commit()
    logger.debug(post_to_update)
    return post_query.first()
