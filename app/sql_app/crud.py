import datetime
from datetime import datetime
from passlib.context import CryptContext
from services import email
from sqlalchemy import select, Table, MetaData, text
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine

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
    error = False
    user = db.query(models.User).filter(models.User.id_social == id_social).first()

    try:
        user.type = type_user
        db.commit()
    except:
        error = True
    return user, error


def ranking(db: Session):
    metadata = MetaData()
    metadata.bind = engine
    view = Table("ranking", metadata, autoload=True)
    query = select([view]).where()
    result = db.execute(query)
    rows = result.all()
    return rows


def user_data(db: Session, iduser: int):
    metadata = MetaData()
    metadata.bind = engine
    result = db.execute(text("""SELECT * FROM ranking WHERE idUser = """ + str(iduser)))
    row = result.first()
    return row


def create_user(db: Session, user: schemas.UserCreate):
    error = False
    users = None
    try:
        hashed_password = pwd_context.hash(f"{datetime.now()}")

        if "@ifnmg.edu.br" in user.email:
            users = models.User(given_name=user.given_name, family_name=user.family_name, email=user.email, type=1,
                                password=hashed_password,
                                id_social=user.id_social)

        else:
            users = models.User(given_name=user.given_name, family_name=user.family_name, email=user.email,
                                password=hashed_password, id_social=user.id_social)

        db.add(users)
        db.commit()
        db.refresh(users)
    except:
        error = True
    return users, error


# -----------------------------------------------------------------------------------


# ----------------------------------- CRUD Badges -----------------------------------
def badges_status(db: Session, iduser: int):
    metadata = MetaData()
    metadata.bind = engine
    result = db.execute(text(f"""
    SELECT 
    Badge.idBadge, Badge.Name AS name, Badge.Description as description, Badge.Date_Create as date_create, Badge.Date_End as date_end, r.Name as rarity,
    IF(Badge.idBadge IN (SELECT 
                Badge_idBadge
            FROM
                stats
            WHERE
                User_idUser = {iduser}),
        'Adquirida',
        'Não Adquirida') AS situacao
    FROM
    Badge iNNER JOIN Rarity as r ON (Badge.Rarity_idRarity = r.idRarity) WHERE (SELECT XP FROM ranking WHERE idUser = {iduser}) >= r.Min_XP ORDER BY situacao
    """))
    badges = result.all()
    return badges


def get_badges(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Badge).offset(skip).limit(limit).all()


def get_badge_by_id(db: Session, id_badge: int):
    return db.query(models.Badge).filter(models.Badge.idBadge == id_badge).first()


def get_badge_by_user(db: Session, id_social: str):
    user = get_user_by_id_social(db, id_social=id_social)
    if not user:
        return None, True
    return db.query(models.Badge).filter(models.Badge.User_idUser == user.idUser).all(), False


def create_user_badge(db: Session, badge: schemas.Badge):
    error = False
    try:
        badges = models.Badge(name=badge.name, description=badge.description, User_idUser=badge.User_idUser,
                              Rarity_idRarity=badge.Rarity_idRarity)

        user = db.query(models.User).filter(models.User.idUser == badge.User_idUser).first()

        db.add(badges)
        db.commit()
        db.refresh(badges)
        email.send_email(email_receiver=user.email, id_badge=badges.idBadge,
                         title=badges.name, description=badges.description)
    except:
        error = True
    return error


# ----------------------------------- CRUD Stats -----------------------------------
def get_stats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Stats).offset(skip).limit(limit).all()


def get_stats_by_user_social_id(db: Session, social_id_user: str):
    user = get_user_by_id_social(db, social_id_user)
    if user:
        return db.query(models.Stats).filter(models.Stats.User_idUser == user.idUser).all(), False
    else:
        return None, True


def create_stats(db: Session, stats_create: schemas.StatsCreate):
    error = False
    stats = None
    try:
        stats = db.query(models.Stats).filter(models.Stats.Badge_idBadge == stats_create.Badge_idBadge,
                                              models.Stats.User_idUser == stats_create.User_idUser).first()
        if not stats:
            stats = models.Stats(Badge_idBadge=stats_create.Badge_idBadge, User_idUser=stats_create.User_idUser)

            db.add(stats)
            db.commit()
            db.refresh(stats)
    except:
        error = True
    return stats, error


# ----------------------------------- CRUD Rarity -----------------------------------
def get_rarity(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Rarity).offset(skip).limit(limit).all()


def get_rarity_by_id(db: Session, id_rarity: int):
    return db.query(models.Rarity).filter(models.Rarity.idRarity == id_rarity).first()
