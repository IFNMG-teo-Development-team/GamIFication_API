from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from services.token import JWTBearer
from sql_app import schemas
from sql_app.crud import get_users, get_user_by_id_social, change_type_user, ranking
from sql_app.main import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(JWTBearer())],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Ranking],
            summary="Retorna todos os usuários no ranking ordenados por XP")
async def read_users(db: Session = Depends(get_db)):
    return ranking(db)


@router.get("/{id_social}", status_code=status.HTTP_200_OK, response_model=schemas.User,
            summary="Retorna os dados do usuário pelo Id social")
async def read_user(id_social: str, db: Session = Depends(get_db)):
    return get_user_by_id_social(db, id_social=id_social)


@router.patch("/{id_social}", status_code=status.HTTP_200_OK, response_model=schemas.User,
              summary="Altera o tipo do usuário")
async def update_type_user(id_social: str, type_user: int, db: Session = Depends(get_db)):
    user, error = change_type_user(db, type_user=type_user, id_social=id_social)
    if error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="There was a problem when update a user")
    return user
