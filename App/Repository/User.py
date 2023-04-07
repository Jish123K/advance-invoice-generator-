from typing import List

from fastapi import status, HTTPException

from sqlalchemy.orm import Session

from sqlalchemy import exists

from .. import models, schemas, utils

def create_user(user: schemas.UserCreate, db: Session):

    hashed_password = utils.hash(user.password)

    user.password = hashed_password

    if db.query(exists().where(models.User.email == user.email)).scalar() or \

            db.query(exists().where(models.User.username == user.username)).scalar():

        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    new_user = models.User(**user.dict())

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user

def get_user(id: int, db: Session):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")

    return user

def get_user_all(db: Session):

    users = db.query(models.User).all()

    if not users:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")

    return users

