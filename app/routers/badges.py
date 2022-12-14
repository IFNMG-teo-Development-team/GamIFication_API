from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from services.token import JWTBearer
from sql_app import schemas
from sql_app.crud import create_user_badge
from sql_app.crud import get_badges
from sql_app.crud import get_badge_by_id, get_badge_by_user, get_user_by_id_social, badges_status
from sql_app.main import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/badges",
    tags=["badges"],
    dependencies=[Depends(JWTBearer())],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Badge],
            summary="Retorna todas as badges já cadastradas")
async def read_badges(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_badges(db, skip=skip, limit=limit)


@router.get("/my/{user_id_social}", status_code=status.HTTP_200_OK, response_model=List[schemas.BadgesMy],
            summary="Retorna todas as badges indicando se foi adquirida ou não pelo usuário")
async def read_my_badges(user_id_social: str, db: Session = Depends(get_db)):
    user = get_user_by_id_social(db, user_id_social)
    return badges_status(db, user.idUser)


@router.get("/{user_id_social}", status_code=status.HTTP_200_OK, response_model=List[schemas.Badge],
            summary="Retorna as badges cadastradas por um professor")
async def read_badges_by_user(user_id_social: str, db: Session = Depends(get_db)):
    badges, error = get_badge_by_user(db, id_social=user_id_social)
    if error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There was a problem")
    return badges


@router.post("/", status_code=status.HTTP_200_OK, response_model=schemas.BadgeCreate,
             summary="Cria uma nova badge")
async def create_badge(db: Session = Depends(get_db), badge: schemas.BadgeCreate = None):
    create_user_badge(db, badge)
    return badge
