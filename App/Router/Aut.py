from fastapi import APIRouter, Depends, HTTPException

from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy.orm import Session

from app.repository import auth

from .. import database, schemas

from jose import jwt, JWTError

from passlib.context import CryptContext

router = APIRouter(tags=['Authentication'])

security = HTTPBasic()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"

SECRET_KEY = "mysecretkey"

@router.post('/login', response_model=schemas.Token)

def logs(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(database.get_db)):

    user = auth.authenticate_user(db, credentials.username, credentials.password)

    if not user:

        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}

def create_access_token(data: dict, expires_delta: int = 30):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=expires_delta)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

