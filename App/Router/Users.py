from typing import List

from fastapi import status, HTTPException, Depends, APIRouter

from sqlalchemy import create_engine, text

from sqlalchemy.orm import sessionmaker

from sqlalchemy.engine.url import URL

from .. import models, schemas, utils

from ..database import get_db

router = APIRouter(

    prefix="/users",

    tags=['Users']

)

# database connection URL

DATABASE_URL = "postgresql://user:password@localhost/dbname"

# create the engine

engine = create_engine(DATABASE_URL)

# create a SessionLocal class

SessionLocal = sessionmaker(bind=engine)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)

def create_usr(users: schemas.UserCreate, db: Session = Depends(get_db)):

    try:

        # create a new user record

        stmt = text("INSERT INTO users (name, email, password) VALUES (:name, :email, :password)")

        with engine.connect() as conn:

            conn.execute(stmt, name=users.name, email=users.email, password=utils.hash_password(users.password))

        # get the created user and return it

        stmt = text("SELECT * FROM users WHERE email=:email")

        with engine.connect() as conn:

            result = conn.execute(stmt, email=users.email).fetchone()

        return dict(result)

    

    except Exception as e:

        # handle exceptions

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('/{id}', response_model=schemas.UserInvoices)

def get_use(id: int, db: Session = Depends(get_db), ):

    try:

        # get a user and their invoices by id

        stmt = text("SELECT u.*, i.* FROM users u JOIN invoices i ON u.id=i.user_id WHERE u.id=:id")

        with engine.connect() as conn:

            result = conn.execute(stmt, id=id).fetchall()

        return [dict(row) for row in result]

    

    except Exception as e:

        # handle exceptions

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('/', response_model=List[schemas.UserInvoices])

def get_user_all(db: Session = Depends(get_db)):

    try:

        # get all users and their invoices

        stmt = text("SELECT u.*, i.* FROM users u JOIN invoices i ON u.id=i.user_id")

        with engine.connect() as conn:

            result = conn.execute(stmt).fetchall()

        return [dict(row) for row in result]

    

    except Exception as e:

        # handle exceptions

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

