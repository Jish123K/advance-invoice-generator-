from fastapi import Depends, status, HTTPException

from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from passlib.context import CryptContext

from datetime import datetime, timedelta

from jose import JWTError, jwt

from .. import models, oauth2

from ..database import get_db

SECRET_KEY = "your-secret-key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(

    prefix="/login",

    tags=['Authentication']

)

@router.post("/")

def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):

    user = db.query(models.User).filter((models.User.email == form_data.username) | (models.User.username == form_data.username)).first()

    if not user:

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not pwd_context.verify(form_data.password, user.password):

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token_subject = str(user.id)

    access_token_issued_at = datetime.utcnow()

    access_token_expires_at = access_token_issued_at + access_token_expires

    access_token_data = {

        "sub": access_token_subject,

        "iat": access_token_issued_at,

        "exp": access_token_expires_at

    }

    access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}

