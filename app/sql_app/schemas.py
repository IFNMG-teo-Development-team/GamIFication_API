from pydantic import BaseModel
from datetime import date, time, datetime


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
    password: str | None

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
