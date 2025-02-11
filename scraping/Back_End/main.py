from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import bcrypt
import jwt
import datetime
from database import get_db, Base, engine
from models import User as UserModel
from models import Product as ProductModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
import requests
from bs4 import BeautifulSoup



# Clé secrète pour la signature du JWT
SECRET_KEY = "ourKey"  # Changez cette clé

# Initialisation de l'application FastAPI
app = FastAPI()

# Middleware CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend Vue.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Modèle Pydantic pour l'utilisateur
class User(BaseModel):
    username: str
    password: str

# Fonction pour générer un JWT
def create_access_token(data: dict):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expire après 1 heure
    to_encode = data.copy()
    to_encode.update({"exp": expiration})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

@app.post("/signup")
def signup(user: User, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà utilisé")

    # Hacher le mot de passe
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Ajouter l'utilisateur à la base de données
    new_user = UserModel(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"Utilisateur {user.username} créé avec succès"}

@app.post("/login")
def login(user: User, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe
    existing_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur ou mot de passe incorrect")

    # Vérifier le mot de passe
    if not bcrypt.checkpw(user.password.encode('utf-8'), existing_user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")

    # Créer un token JWT
    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}
@app.get("/scrape")
def scrape(url: str, image_selector: str, name_selector: str, brand_selector: str, price_selector: str, description_selector: str, reference_selector: str = None):
    try:
        # Faire une requête GET pour obtenir la page
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la requête a réussi
        
        # Utilisation de BeautifulSoup pour parser le HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraire les éléments spécifiques à partir des sélecteurs fournis
        image = soup.select_one(image_selector)
        name = soup.select_one(name_selector)
        brand = soup.select_one(brand_selector)
        price = soup.select_one(price_selector)
        description = soup.select_one(description_selector)

        # Gestion de la référence : si le sélecteur est fourni, l'utiliser
        reference = None
        if reference_selector:
            reference_elem = soup.select_one(reference_selector)
            reference = reference_elem.get_text(strip=True) if reference_elem else None

        # Si la référence n'est toujours pas trouvée, l'extraire de l'URL
        if not reference:
            reference = url.split('-')[-1].replace('.html', '')

        # Fonction pour extraire le texte ou l'attribut d'un élément
        def extract_element_text_or_attr(element, attr=None):
            if not element:
                return None
            if attr and attr in element.attrs:
                return element[attr]
            return element.get_text(strip=True)

        # Extraire les informations en utilisant la fonction générique
        product_info = {
            'image': extract_element_text_or_attr(image, 'src'),
            'name': extract_element_text_or_attr(name),
            'brand': extract_element_text_or_attr(brand, 'alt'),  # Utiliser 'alt' si c'est une image
            'reference': reference if reference else "Référence non trouvée",
            'price': extract_element_text_or_attr(price),
            'description': extract_element_text_or_attr(description)
        }

        # Vérifier si toutes les informations essentielles sont présentes
        if all(product_info.values()):
            return {"product_info": product_info}
        else:
            raise HTTPException(status_code=404, detail="Un ou plusieurs éléments spécifiés n'ont pas été trouvés")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'extraction des informations: {e}")


# Modèle Pydantic pour le produit
class Product(BaseModel):
    image: str
    name: str
    brand: str
    reference: str
    price: str
    description: str

@app.post("/products/")
def create_product(product: Product, db: Session = Depends(get_db)):
    db_product = ProductModel(
        image=product.image,
        name=product.name,
        brand=product.brand,
        reference=product.reference,
        price=product.price,
        description=product.description
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/")
def get_products(db: Session = Depends(get_db)):
    products = db.query(ProductModel).all()
    return products


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    # Trouver le produit à supprimer
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    # Supprimer le produit
    db.delete(product)
    db.commit()
    return {"message": "Produit supprimé avec succès"}
