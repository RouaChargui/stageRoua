from sqlalchemy import Column, Integer, String, Text
from database import Base

# Modèle SQLAlchemy pour la table "users"
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)


# Modèle SQLAlchemy pour la table "products"
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String(255), nullable=True)
    name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=True)
    reference = Column(String(255), nullable=True)
    price = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)