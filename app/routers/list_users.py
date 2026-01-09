from fastapi import APIRouter, Depends
from app.db.database import get_session
from app.models.model_user import User
from app.schemas.public.user_public import UserPublic
from sqlalchemy.orm import Session
from typing import List

routers = APIRouter(prefix='/routers', tags=['routers'])

@routers.get(
    path='/users',
    response_model=List[UserPublic]
)
def list_users(
    session: Session = Depends(get_session)
):
    database = session.query(User).all()
    return database
