from typing import List

from fastapi import APIRouter, Depends, status
from services.token import JWTBearer
from sql_app import schemas
from sql_app.crud import create_user_badge
from sql_app.crud import get_badges
from sql_app.crud import get_gadge_by_id
from sql_app.main import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/badges",
    tags=["badges"],
    dependencies=[Depends(JWTBearer())],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Badge])
async def read_badges(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_badges(db, skip=skip, limit=limit)


@router.get("/{id_badge}", status_code=status.HTTP_200_OK, response_model=schemas.Badge)
async def read_badge(id_badge: int, db: Session = Depends(get_db)):
    return get_gadge_by_id(db, id_badge=id_badge)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BadgeCreate)
async def create_badge(db: Session = Depends(get_db), badge: schemas.BadgeCreate = None):
    create_user_badge(db, badge)
    return badge
