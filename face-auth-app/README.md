# Face Auth App

Application d'authentification par reconnaissance faciale avec Electron.js et Python.

## 🚀 Fonctionnalités

- **Interface moderne Electron.js** - Interface utilisateur élégante et responsive
- **Inscription avec reconnaissance faciale** - Enregistrement des utilisateurs avec capture de visage
- **Connexion double authentification** :
  - Connexion classique (nom d'utilisateur + mot de passe)
  - Connexion par reconnaissance faciale
- **Base de données MySQL** - Stockage sécurisé des utilisateurs et données faciales
- **API REST FastAPI** - Backend robuste avec validation et sécurité

## 🛠️ Technologies utilisées

### Frontend
- **Electron.js** - Framework pour applications desktop
- **HTML5/CSS3/JavaScript** - Interface utilisateur moderne
- **WebRTC API** - Accès à la caméra pour capture d'images

### Backend
- **Python 3.8+** - Langage de développement
- **FastAPI** - Framework API moderne et rapide
- **SQLAlchemy** - ORM pour la base de données
- **face_recognition** - Bibliothèque de reconnaissance faciale
- **OpenCV** - Traitement d'images
- **bcrypt** - Hachage sécurisé des mots de passe

### Base de données
- **MySQL 8.0+** - Base de données relationnelle

## 📋 Prérequis

### Système
- **Python 3.8+**
- **Node.js 16+**
- **MySQL 8.0+**
- **Caméra web** (pour la reconnaissance faciale)

### Dépendances système (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3-dev cmake libopenblas-dev liblapack-dev
sudo apt-get install libgtk-3-dev libboost-python-dev
```

### Dépendances système (macOS)
```bash
brew install cmake
```

### Dépendances système (Windows)
- Visual Studio Build Tools
- CMake

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone <url-du-repo>
cd face-auth-app
```

### 2. Configuration de la base de données
```bash
# Connexion à MySQL
mysql -u root -p

# Exécuter le script d'initialisation
source database/init.sql
```

### 3. Configuration du backend
```bash
cd backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Modifier .env avec vos paramètres de base de données
```

### 4. Configuration du frontend
```bash
cd ../frontend

# Installer les dépendances Node.js
npm install
```

## 🎯 Utilisation

### 1. Démarrer le backend
```bash
cd backend
source venv/bin/activate  # Linux/macOS
# ou venv\Scripts\activate  # Windows

python main.py
```
Le serveur API sera accessible sur `http://localhost:8000`

### 2. Démarrer l'application Electron
```bash
cd frontend
npm start
```

### 3. Utilisation de l'application

1. **Inscription** :
   - Remplir les informations (nom d'utilisateur, email, mot de passe)
   - Capturer une photo claire de votre visage
   - Valider l'inscription

2. **Connexion** :
   - **Méthode classique** : Nom d'utilisateur + mot de passe
   - **Reconnaissance faciale** : Nom d'utilisateur + capture de visage

## 🔧 Configuration

### Variables d'environnement (.env)
```env
DATABASE_URL=mysql+pymysql://username:password@localhost/face_auth_db
```

### Configuration de la base de données
Modifier les paramètres dans `backend/database.py` si nécessaire.

## 🏗️ Architecture

```
face-auth-app/
├── backend/                 # API Python FastAPI
│   ├── main.py             # Point d'entrée de l'API
│   ├── database.py         # Configuration base de données
│   ├── face_recognition_service.py  # Service reconnaissance faciale
│   ├── requirements.txt    # Dépendances Python
│   └── .env               # Variables d'environnement
├── frontend/               # Application Electron
│   ├── main.js            # Point d'entrée Electron
│   ├── package.json       # Configuration Node.js
│   └── src/
│       ├── pages/         # Pages HTML
│       ├── styles/        # Fichiers CSS
│       └── js/           # Scripts JavaScript
└── database/
    └── init.sql          # Script d'initialisation MySQL
```

## 🔒 Sécurité

- **Mots de passe** : Hachage bcrypt avec sel
- **Reconnaissance faciale** : Encodages stockés de manière sécurisée
- **API** : Validation des données d'entrée
- **CORS** : Configuration restrictive en production

## 🐛 Dépannage

### Erreurs communes

1. **Erreur de connexion à la base de données** :
   - Vérifier que MySQL est démarré
   - Vérifier les paramètres de connexion dans `.env`

2. **Erreur de reconnaissance faciale** :
   - Vérifier que la caméra est accessible
   - S'assurer d'un bon éclairage pour la capture

3. **Problèmes d'installation face_recognition** :
   - Installer les dépendances système requises
   - Utiliser Python 3.8-3.9 pour une meilleure compatibilité

### Logs
- Backend : Logs dans la console Python
- Frontend : DevTools Electron (F12)

## 📖 API Documentation

Avec le backend en cours d'exécution, accéder à :
- **Documentation interactive** : http://localhost:8000/docs
- **OpenAPI JSON** : http://localhost:8000/openapi.json

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les modifications (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Support

Pour toute question ou problème :
- Créer une issue sur GitHub
- Consulter la documentation API
- Vérifier les logs d'erreur