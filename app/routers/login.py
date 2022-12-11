from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from services.token import JWTRepo
from sql_app import schemas
from sql_app.crud import create_user, get_user_by_id_social
from sql_app.main import get_db
from sql_app.schemas import TokenResponse, ResponseSchema
from sql_app.schemas import UserToken

router = APIRouter(
    prefix="/auth",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=status.HTTP_200_OK, response_model=UserToken)
async def auth_user(db: Session = Depends(get_db), user: schemas.UserCreate = None):
    auth = get_user_by_id_social(db, user.id_social)
    if auth is None:
        auth = create_user(db, user)
    token = JWTRepo.generate_token({'sub': auth.id_social})

    return UserToken(
        idUser=auth.idUser, type=auth.type, given_name=auth.given_name, family_name=auth.family_name, email=auth.email,
        id_social=auth.id_social,
        result=TokenResponse(access_token=token, token_type="Bearer")).dict(exclude_none=True)
