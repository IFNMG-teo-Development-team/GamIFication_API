from datetime import datetime
from typing import Optional, Dict, Any
from typing import TypeVar
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
        schema_extra = {
            "example": {
                "idBadge": 1,
                "name": "Realizar TCC II",
                "date_create": "2022-12-11 12:57:12",
                "date_end": "2022-12-11 12:57:12",
                "description": "Informações sobre a badge",
                "Rarity_idRarity": 1,
                "User_idUser": 5
            }
        }
        orm_mode = True


class BadgesMy(BaseModel):
    idBadge: int
    name: str
    date_create: datetime
    date_end: datetime
    description: str
    rarity: str
    situacao: str

    class Config:
        schema_extra = {
            "example": {
                "idBadge": 1,
                "name": "Realizar TCC II",
                "date_create": "2022-12-11 12:57:12",
                "date_end": "2022-12-11 12:57:12",
                "description": "Informações sobre a badge",
                "rarity": "Bronze",
                "situacao": "Não Adquirida"
            }
        }
        orm_mode = True


class BadgeCreate(BaseModel):
    name: str
    date_end: datetime
    description: str
    Rarity_idRarity: int
    User_idUser: int

    class Config:
        schema_extra = {
            "example": {
                "idBadge": 1,
                "name": "Realizar TCC I",
                "date_end": "2022-12-11 12:57:12",
                "description": "Informações sobre a badge",
                "Rarity_idRarity": 1,
                "User_idUser": 5
            }
        }
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


class UserToken(BaseModel):
    idUser: int
    XP: Optional[T] = None
    Nivel: Optional[T] = None
    type: int
    given_name: str
    family_name: str
    email: str
    id_social: str
    result: Optional[T] = None

    class Config:
        schema_extra = {
            "example": {
                "idUser": 1,
                "XP": 200,
                "Nivel": "Bronze",
                "type": 2,
                "given_name": "Calvin",
                "family_name": "IFeno",
                "email": "calvif@gmail.com",
                "id_social": "32192sdas90we",
                "result": {
                    "access_token": "asdasiojdhasidoasdaisdoasdaosidjasdhaidguaudgausdgasdiaugsdiadghaisdugasiudgasdiuasgdidgiasdg",
                    "token_type": "Bearer"
                }
            }
        }
        orm_mode = True


class Ranking(BaseModel):
    idUser: int
    Nivel: str
    XP: int
    given_name: str
    family_name: str

    class Config:
        schema_extra = {
            "example":
                [
                    {
                        "idUser": 6,
                        "Nivel": "Prata",
                        "XP": 1000,
                        "given_name": "teste",
                        "family_name": "1"
                    },
                    {
                        "idUser": 7,
                        "Nivel": "Bronze",
                        "XP": 800,
                        "given_name": "teste",
                        "family_name": "2"
                    },
                    {
                        "idUser": 5,
                        "Nivel": "Bronze",
                        "XP": 200,
                        "given_name": "teste",
                        "family_name": "3"
                    },
                    {
                        "idUser": 10,
                        "Nivel": "Bronze",
                        "XP": 200,
                        "given_name": "teste",
                        "family_name": "4"
                    }
                ]
        }

        orm_mode = True
