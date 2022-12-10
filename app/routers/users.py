from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Dict

from sql_app import schemas, models
from sql_app.crud import get_users, get_user_by_id_social, change_type_user
from sql_app.main import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db, skip=skip, limit=limit)


@router.get("/{id_social}", status_code=status.HTTP_200_OK, response_model=schemas.User)
async def read_user(id_social: str, db: Session = Depends(get_db)):
    return get_user_by_id_social(db, id_social=id_social)


@router.patch("/{id_social}", status_code=status.HTTP_200_OK, response_model=schemas.User)
async def update_type_user(id_social: str, type_user: int, db: Session = Depends(get_db)):
    return change_type_user(db, type_user=type_user, id_social=id_social)
