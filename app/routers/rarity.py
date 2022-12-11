from typing import List

from fastapi import APIRouter, Depends, status
from services.token import JWTBearer
from sql_app import schemas
from sql_app.crud import get_rarity, get_rarity_by_id
from sql_app.main import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/rarity",
    tags=["rarity"],
    dependencies=[Depends(JWTBearer())],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Rarity])
async def read_rarities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_rarity(db, skip=skip, limit=limit)


@router.get("/{id_rarity}", status_code=status.HTTP_200_OK, response_model=schemas.Rarity)
async def read_rarity(id_rarity: int, db: Session = Depends(get_db)):
    return get_rarity_by_id(db, id_rarity)
