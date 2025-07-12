from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime
import uvicorn

from database import get_db, create_tables, User
from face_recognition_service import FaceRecognitionService

app = FastAPI(title="Face Authentication API", version="1.0.0")

# Configuration CORS pour permettre les requêtes depuis Electron
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration du hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modèles Pydantic
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    face_image: str  # Image en base64

class UserLogin(BaseModel):
    username: str
    password: str

class FaceLogin(BaseModel):
    username: str
    face_image: str  # Image en base64

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@app.on_event("startup")
async def startup_event():
    create_tables()

@app.get("/")
async def root():
    return {"message": "Face Authentication API is running"}

@app.post("/api/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Inscription d'un nouvel utilisateur avec reconnaissance faciale
    """
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur ou email déjà utilisé")
    
    # Encoder le visage
    face_encoding = FaceRecognitionService.encode_face_from_base64(user_data.face_image)
    if face_encoding is None:
        raise HTTPException(status_code=400, detail="Aucun visage détecté dans l'image. Veuillez réessayer avec une photo claire de votre visage.")
    
    # Créer l'utilisateur
    hashed_password = hash_password(user_data.password)
    serialized_face_encoding = FaceRecognitionService.serialize_encoding(face_encoding)
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        face_encoding=serialized_face_encoding
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        is_active=new_user.is_active,
        created_at=new_user.created_at
    )

@app.post("/api/login")
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Connexion traditionnelle avec nom d'utilisateur et mot de passe
    """
    user = db.query(User).filter(User.username == login_data.username).first()
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")
    
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Compte désactivé")
    
    # Mettre à jour la dernière connexion
    user.last_login = datetime.utcnow()
    db.commit()
    
    return {
        "message": "Connexion réussie",
        "user": UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at
        )
    }

@app.post("/api/face-login")
async def face_login(face_data: FaceLogin, db: Session = Depends(get_db)):
    """
    Connexion par reconnaissance faciale
    """
    user = db.query(User).filter(User.username == face_data.username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Compte désactivé")
    
    if not user.face_encoding:
        raise HTTPException(status_code=400, detail="Aucune donnée faciale enregistrée pour cet utilisateur")
    
    # Vérifier le visage
    is_match, message = FaceRecognitionService.verify_face(user.face_encoding, face_data.face_image)
    
    if not is_match:
        raise HTTPException(status_code=401, detail=f"Reconnaissance faciale échouée: {message}")
    
    # Mettre à jour la dernière connexion
    user.last_login = datetime.utcnow()
    db.commit()
    
    return {
        "message": f"Connexion par reconnaissance faciale réussie. {message}",
        "user": UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at
        )
    }

@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Récupérer les informations d'un utilisateur
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)