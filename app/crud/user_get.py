from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from app.models.model_user import User
from app.schemas.public.user_public import UserPublic
from app.db.database import get_session

get_router = APIRouter(
    prefix='/api/users', 
    tags=['users']
)

@get_router.get(
    path='/{user_id}',
    response_model=UserPublic
)
def get_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    data = session.query(User).filter(User.id == user_id).first()
    if not data:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found"
        )
    
    return data
