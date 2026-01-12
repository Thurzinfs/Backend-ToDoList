from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_session
from app.models.model_user import User
from app.models.model_token import Token
from app.core.security import verify_password, create_access_token, create_refresh_token, hash_token, REFRESH_TOKEN_EXPIRE_DAYS, SECRET_KEY, ALGORITMO
from app.schemas.token.schema_token import Token as TokenPublic
from app.schemas.schemas.refresh_token import RefreshTokenIn
from app.core.security import get_current_user
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from http import HTTPStatus
import jwt

auth_router = APIRouter(prefix="/auth", tags=['auth'])

@auth_router.post(
    path="/token",
    response_model=TokenPublic
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid email or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token = create_access_token(
        data= {
            'sub' : str(user.id),
            'type' : 'access'
        }
    )
    refresh_token = create_refresh_token(
        data= {
            'sub' : str(user.id),
            'type' : 'refresh'
        }
    )

    token_db = Token(
        user_id = user.id,
        token_hash = hash_token(refresh_token),
        expire_at = datetime.now(tz=ZoneInfo('UTC')) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        revoked = False
    )

    session.add(token_db)
    session.commit()

    return {
        'access_token' : access_token,
        'refresh_token' : refresh_token,
        'token_type' : 'Bearer'
    }

@auth_router.post(
    path='/refresh/token',
    response_model=TokenPublic
)
def refresh_token(
    data: RefreshTokenIn,
    session: Session = Depends(get_session)
):
    try:
        text_refresh_token = data.refresh_token

        payload = jwt.decode(
            text_refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITMO]
        )

        user_id = payload.get('sub')
        token_type = payload.get('type')

        if user_id is None or token_type != 'refresh':
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid token')
        
        token_hash = hash_token(text_refresh_token)

        token_db = session.query(Token).filter(Token.token_hash == token_hash, Token.revoked == False).first()

        if not token_db:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Refresh token revoked or not found")

        if token_db.expire_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Refresh token expired")
        
        session.query(Token).filter(Token.user_id == int(user_id), Token.revoked == False).update({Token.revoked: True}, synchronize_session=False)        

        new_access_token = create_access_token(
            data= {
                'sub' : payload.get('sub'),
                'type' : 'access'
            }
        )
        new_refresh_token = create_refresh_token(
            data= {
                'sub' : payload.get('sub'),
                'type' : 'refresh'
            }
        )

        token_db = Token(
            user_id = int(user_id),
            token_hash = hash_token(new_refresh_token),
            expire_at = datetime.now(tz=ZoneInfo('UTC')) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            revoked = False
        )

        session.add(token_db)
        session.commit()

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "Bearer"
        }

    except jwt.PyJWTError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid token')

@auth_router.get(
    path='/me',
)
def me(current_user = Depends(get_current_user)):
    return current_user