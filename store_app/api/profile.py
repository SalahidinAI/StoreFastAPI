from sqlalchemy.orm import Session
from store_app.db.database import SessionLocal
from store_app.db.models import UserProfile
from store_app.db.schema import UserProfileSchema
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

user_router = APIRouter(prefix='/user', tags=['Users'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.post('/', response_model=UserProfileSchema)
async def user_create(user: UserProfileSchema, db: Session = Depends(get_db)):
    user_db = UserProfile(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@user_router.get('/', response_model=List[UserProfileSchema])
async def user_list(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()


@user_router.get('/{user_id}/', response_model=UserProfileSchema)
async def user_detail(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user_db


@user_router.put('/{user_id}/', response_model=UserProfileSchema)
async def user_update(user_id: int, user: UserProfileSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail='User not found')

    for user_key, user_value in user.dict().items():
        setattr(user_db, user_key, user_value)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@user_router.delete('/{user_id}/')
async def user_delete(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(user_db)
    db.commit()
    return {'message': 'user is deleted'}
