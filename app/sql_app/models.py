from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME, func
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "User"

    idUser = Column(Integer, primary_key=True, index=True)
    type = Column(Integer, default=0)
    given_name = Column(String)
    family_name = Column(String)
    email = Column(String)
    password = Column(String)
    id_social = Column(String)

    Badge = relationship("Badge", back_populates="creator")
    creator = relationship("Stats", back_populates="creator")


class Badge(Base):
    __tablename__ = "Badge"

    idBadge = Column(Integer, primary_key=True, index=True)
    # xp = Column(Integer)
    name = Column(String)
    date_create = Column(DATETIME, default=func.now())
    date_end = Column(DATETIME, default=func.now())
    description = Column(String)
    User_idUser = Column(Integer, ForeignKey("User.idUser"))
    Rarity_idRarity = Column(Integer, ForeignKey("Rarity.idRarity"), default=1)

    creator = relationship("User", back_populates="Badge")
    badge_rarity = relationship("Rarity", back_populates="Badge")

    badge_stats = relationship("Stats", back_populates="badge_stats")


class Rarity(Base):
    __tablename__ = "Rarity"

    idRarity = Column(Integer, primary_key=True, index=True)
    XP = Column(Integer)
    Icon = Column(String, default=None)
    Name = Column(String)
    Min_XP = Column(String, default=None)

    Badge = relationship("Badge", back_populates="badge_rarity")


class Stats(Base):
    __tablename__ = "stats"

    ID = Column(Integer, primary_key=True, index=True)
    Date_Acquirement = Column(DATETIME, default=func.now())
    Badge_idBadge = Column(Integer, ForeignKey("Badge.idBadge"))
    User_idUser = Column(Integer, ForeignKey("User.idUser"))

    creator = relationship("User", back_populates="creator")
    badge_stats = relationship("Badge", back_populates="badge_stats")
