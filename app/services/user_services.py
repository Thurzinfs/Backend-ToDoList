from sqlalchemy.orm import Session
from app.models.model_user import User
from app.core.security import get_password_hash
from fastapi import HTTPException
from http import HTTPStatus

def create_user_service(session: Session, user_data: dict):
    user_existing = session.query(User).filter(User.email == user_data['email']).first()
    if user_existing:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Email already registered")
    
    data = User(
        nome = user_data['nome'],
        email = user_data['email'],
        password = get_password_hash(user_data['password'])
    )

    session.add(data)
    session.commit()
    session.refresh(data)
    return data

def update_put_user_service(session: Session, user_data: dict, user_id: int, current_user):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Forbidden: insufficient permissions"
        )
    
    current_user.nome = user_data['nome']
    current_user.email = user_data['email']
    current_user.password = get_password_hash(user_data['password'])

    session.commit()
    session.refresh(current_user)
    return current_user

def patch_user_service(session: Session, user_data: dict, user_id: int, current_user):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Forbidden: insufficient permissions"
        )
    
    for field, value in user_data.items():
        if field == "password":
            value = get_password_hash(value)

        setattr(current_user, field, value)

    session.commit()
    session.refresh(current_user)
    return current_user

def delete_user_service(session: Session, user_id: int, current_user):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Forbidden: insufficient permissions"
        )
    
    session.delete(current_user)
    session.commit()
    return {
        'msg' : 'User deleted'
    }