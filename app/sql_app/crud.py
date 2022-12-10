import datetime
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime
from dotenv import load_dotenv
from . import models, schemas
from services import email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ----------------------------------- CRUD User -----------------------------------
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.idUser == user_id).first()


def get_user_by_id_social(db: Session, id_social: str):
    return db.query(models.User).filter(models.User.id_social == id_social).first()


def auth(db: Session, id_social: models.User.id_social):
    return db.query(models.User).filter(models.User.idUser == id_social).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def change_type_user(db: Session, type_user: int, id_social: str):
    user = db.query(models.User).filter(models.User.id_social == id_social).first()
    user.type = type_user
    db.commit()
    return user


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(f"{datetime.now()}")

    if "@ifnmg.edu.br" in user.email:
        users = models.User(given_name=user.given_name, family_name=user.family_name, email=user.email, type=1, password=hashed_password,
                            id_social=user.id_social)

    else:
        users = models.User(given_name=user.given_name, family_name=user.family_name, email=user.email, password=hashed_password, id_social=user.id_social)
    db.add(users)
    db.commit()
    db.refresh(users)
    return users


# -----------------------------------------------------------------------------------


# ----------------------------------- CRUD Badges -----------------------------------
def get_badges(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Badge).offset(skip).limit(limit).all()


def get_gadge_by_id(db: Session, id_badge: int):
    return db.query(models.Badge).filter(models.Badge.idBadge == id_badge).first()


def create_user_badge(db: Session, badge: schemas.Badge):
    badges = models.Badge(name=badge.name, description=badge.description, User_idUser=badge.User_idUser,
                          Rarity_idRarity=badge.Rarity_idRarity)

    user = db.query(models.User).filter(models.User.idUser == badge.User_idUser).first()

    db.add(badges)
    db.commit()
    db.refresh(badges)
    email.send_email(email_receiver=user.email, id_badge=badges.idBadge)
