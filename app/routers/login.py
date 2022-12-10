from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..sql_app import schemas
from ..sql_app.crud import create_user, get_user_by_id_social
from ..sql_app.main import get_db

router = APIRouter(
    prefix="/auth",
    tags=["users"],
    # dependencies=[Depends(get_db())],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.UserCreate, status_code=status.HTTP_200_OK)
async def auth_user(db: Session = Depends(get_db), user: schemas.UserCreate = None):
    auth = get_user_by_id_social(db, user.id_social)
    if auth is None:
        auth = create_user(db, user)
    return auth
