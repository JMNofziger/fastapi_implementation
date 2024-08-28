from fastapi import FastAPI
from models import Base
from database import engine
from routers import post, user, auth, vote
from config import settings, logger

# with alembic the intialization of tables with sqlalchemy isn't needed
# initialize/create all the defined models for tables
# Base.metadata.create_all(bind=engine)

# initialize FastAPI app
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
