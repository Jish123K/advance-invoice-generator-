from datetime import datetime, timedelta

from fastapi import Depends, status, HTTPException

from fastapi_jwt_auth import AuthJWT

from sqlalchemy.orm import Session

from . import schemas, database, models

from .config import settings

SECRET_KEY = settings.secret_key

ALGORITHM = settings.algorithm

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Configure FastAPIJWTAuth

class AuthHandler:

    async def authenticate(self, username: str, password: str) -> models.User:

        db_user = database.get_user_by_email(username)

        if db_user is None:

            return None

        if not database.verify_password(password, db_user.password):

            return None

        return db_user

auth_handler = AuthHandler()

# Create FastAPIJWTAuth instance

auth_jwt = AuthJWT(

    secret_key=SECRET_KEY,

    algorithm=ALGORITHM,

    access_token_expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,

    authenticate=auth_handler.authenticate

)

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = auth_jwt.encode(to_encode)

    return encoded_jwt

def get_current_user(Authorize: AuthJWT = Depends()):

    try:

        Authorize.jwt_required()

        token = Authorize.get_raw_jwt()

        user_id = token.get('sub')

        user = database.get_user_by_id(user_id)

        if user is None:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    except HTTPException as e:

        raise e

    except Exception as e:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

