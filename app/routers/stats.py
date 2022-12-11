from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from services.token import JWTBearer
from sql_app import schemas
from sql_app.crud import create_stats, get_stats_by_user_social_id
from sql_app.crud import get_stats
from sql_app.main import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/stats",
    tags=["stats"],
    dependencies=[Depends(JWTBearer())],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Stats])
async def read_all_stats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_stats(db, skip=skip, limit=limit)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Stats)
async def Add_new_stats(db: Session = Depends(get_db), stats_badge: schemas.StatsCreate = None):
    stats, error = create_stats(db, stats_badge)
    if error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="There was a problem when created a new stats")
    return stats


@router.get("/{user_id_social}", status_code=status.HTTP_200_OK, response_model=List[schemas.Stats])
async def read_stats_by_user(db: Session = Depends(get_db), user_id_social=str):
    stats, error = get_stats_by_user_social_id(db, user_id_social)
    if error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="There was a problem when retrieved stats")
    return stats

