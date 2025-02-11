from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import mysql.connector


# URL de connexion à la base de données
DATABASE_NAME = "scraping"
#DATABASE_PASSWORD = "ton_mot_de_passe"  # Remplace par ton mot de passe
#DATABASE_URL = f"mysql+mysqlconnector://root:{DATABASE_PASSWORD}@localhost/{DATABASE_NAME}"  # Change selon ton utilisateur et mot de passe
DATABASE_URL = f"mysql+mysqlconnector://root@localhost/{DATABASE_NAME}" # Change selon ton utilisateur et mot de passe


# Création de la base de données si elle n'existe pas
def create_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Ton utilisateur MySQL
            password=""   # Ton mot de passe MySQL
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        connection.commit()
        print(f"Base de données '{DATABASE_NAME}' créée avec succès.")
    except mysql.connector.Error as e:
        print(f"Erreur lors de la création de la base de données : {e}")
    finally:
        cursor.close()
        connection.close()

# Configuration SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dépendance pour obtenir une session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Appelle la fonction de création de la base de données
create_database()
