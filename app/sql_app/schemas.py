from datetime import datetime
from typing import Optional, TypeVar, Dict, Any
from typing import TypeVar, Iterable, Tuple, Union
from pydantic import BaseModel, Field

T = TypeVar('T')


class Badge(BaseModel):
    idBadge: int
    name: str
    date_create: datetime
    date_end: datetime
    description: str

    Rarity_idRarity: int
    User_idUser: int

    class Config:
        orm_mode = True


class BadgeCreate(BaseModel):
    name: str
    date_create: datetime
    date_end: datetime
    description: str

    Rarity_idRarity: int
    User_idUser: int

    class Config:
        orm_mode = True


class User(BaseModel):
    idUser: int
    type: int
    given_name: str
    family_name: str
    email: str
    id_social: str

    class Config:
        schema_extra = {
            "example": {
                "idUser": 1,
                "type": 2,
                "given_name": "Calvin",
                "family_name": "IFeno",
                "email": "calvif@gmail.com",
                "id_social": "32192sdas90we"
            }
        }
        orm_mode = True


class UserCreate(BaseModel):
    given_name: str
    family_name: str
    email: str
    id_social: str
    password: Any  # str

    class Config:
        schema_extra = {
            "example": {
                "given_name": "Calvin",
                "family_name": "IFeno",
                "email": "calvif@gmail.com",
                "id_social": "32192sdas90we",
            }
        }
        orm_mode = True


class StatsCreate(BaseModel):
    User_idUser: int
    Badge_idBadge: int

    class Config:
        schema_extra = {
            "example": {
                "User_idUser": 2,
                "Badge_idBadge": 1,
            }
        }
        orm_mode = True


class Stats(BaseModel):
    Date_Acquirement: datetime
    User_idUser: int
    Badge_idBadge: int

    class Config:
        schema_extra = {
            "example": {
                "Date_Acquirement": "2022-12-11 12:57:12",
                "User_idUser": 2,
                "Badge_idBadge": 1,
            }
        }
        orm_mode = True


class Rarity(BaseModel):
    idRarity: int
    XP: int
    Icon: Any
    Name: str
    Min_XP: Any  # int

    class Config:
        schema_extra = {
            "example": {
                "idRarity": 1,
                "XP": 10,
                "Icon": "https://linkdaimagem.com",
                "Name": "Bronze",
                "Min_XP": 10,
            }
        }
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class Parameter(BaseModel):
    data: Dict[str, str] = None


class RequestSchema(BaseModel):
    parameter: Parameter = Field(...)


class ResponseSchema(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T] = None
