from fastapi import status, HTTPException, Depends, APIRouter
import models, schemas, utils
from database import get_db
from sqlalchemy.orm import Session
import logging

# all method paths in this file begin with the prefix "users"
router = APIRouter(prefix="/users", tags=["Users"])
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password from user input with bycrypt
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
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
