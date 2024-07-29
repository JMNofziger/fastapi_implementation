from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
import database, schemas, models, utils

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_stored_user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )
    if not db_stored_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    if not utils.verify(user_credentials.password, db_stored_user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    # else create token and return to user
    return {"token": "placeholder"}
