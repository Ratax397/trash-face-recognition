# Application de Reconnaissance Faciale

Une application desktop moderne utilisant Electron.js pour l'interface utilisateur et Python Flask pour le backend, avec reconnaissance faciale et base de données MySQL.

## 🚀 Fonctionnalités

- **Interface moderne** : Interface utilisateur élégante avec Electron.js
- **Inscription sécurisée** : Enregistrement avec capture du visage
- **Connexion par reconnaissance faciale** : Authentification biométrique
- **Base de données MySQL** : Stockage sécurisé des utilisateurs et encodages faciaux
- **API REST** : Backend Python Flask avec endpoints sécurisés
- **Responsive Design** : Interface adaptée à différentes tailles d'écran

## 📋 Prérequis

### Système
- **Node.js** (version 16 ou supérieure)
- **Python 3.8+**
- **MySQL 8.0+**
- **Webcam** pour la reconnaissance faciale

### Dépendances système (Linux)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip python3-dev mysql-server mysql-client
sudo apt install libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1

# CentOS/RHEL
sudo yum install python3-pip python3-devel mysql-server mysql
sudo yum install mesa-libGL glib2 libSM libXext libXrender libgomp
```

## 🛠️ Installation

### 1. Cloner le projet
```bash
git clone <repository-url>
cd face-recognition-app
```

### 2. Configuration de la base de données MySQL
```bash
# Démarrer MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# Créer un utilisateur et une base de données
sudo mysql -u root -p
```

Dans MySQL :
```sql
CREATE DATABASE face_recognition_db;
CREATE USER 'face_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON face_recognition_db.* TO 'face_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Configuration de l'environnement
```bash
# Copier le fichier de configuration
cp backend/.env.example backend/.env

# Éditer la configuration
nano backend/.env
```

Configuration `.env` :
```env
DB_HOST=localhost
DB_USER=face_user
DB_PASSWORD=your_password
DB_NAME=face_recognition_db
PORT=5000
DEBUG=False
```

### 4. Installation des dépendances
```bash
# Dépendances Node.js
npm install

# Dépendances Python
cd backend
pip3 install -r requirements.txt
cd ..
```

## 🚀 Démarrage

### Méthode simple (recommandée)
```bash
./start.sh
```

### Méthode manuelle

#### 1. Démarrer le backend Python
```bash
cd backend
python3 start_server.py
```

#### 2. Démarrer l'application Electron (nouveau terminal)
```bash
npm start
```

## 📖 Utilisation

### Inscription
1. Cliquez sur l'onglet "Inscription"
2. Remplissez le formulaire avec vos informations
3. Cliquez sur "Démarrer la caméra"
4. Placez votre visage dans le cadre et cliquez sur "Capturer le visage"
5. Cliquez sur "S'inscrire"

### Connexion
1. Cliquez sur l'onglet "Connexion"
2. Cliquez sur "Démarrer la caméra"
3. Placez votre visage dans le cadre
4. Cliquez sur "Reconnaître le visage"

## 🏗️ Architecture

```
face-recognition-app/
├── main.js                 # Point d'entrée Electron
├── index.html             # Interface utilisateur
├── styles.css             # Styles CSS
├── renderer.js            # Logique frontend
├── package.json           # Configuration Node.js
├── start.sh              # Script de démarrage
├── backend/
│   ├── app.py            # Application Flask
│   ├── start_server.py   # Script de démarrage backend
│   ├── requirements.txt  # Dépendances Python
│   └── .env.example      # Configuration exemple
└── README.md             # Documentation
```

### Technologies utilisées

#### Frontend (Electron.js)
- **Electron** : Framework pour applications desktop
- **HTML5/CSS3** : Interface utilisateur moderne
- **JavaScript ES6+** : Logique côté client
- **WebRTC** : Accès à la caméra

#### Backend (Python Flask)
- **Flask** : Framework web léger
- **Flask-CORS** : Gestion des requêtes cross-origin
- **face-recognition** : Bibliothèque de reconnaissance faciale
- **OpenCV** : Traitement d'images
- **MySQL Connector** : Connexion à la base de données
- **bcrypt** : Hachage sécurisé des mots de passe

#### Base de données (MySQL)
- **Table `users`** : Informations des utilisateurs
- **Table `face_encodings`** : Encodages faciaux

## 🔧 Configuration avancée

### Variables d'environnement
| Variable | Description | Défaut |
|----------|-------------|---------|
| `DB_HOST` | Hôte MySQL | localhost |
| `DB_USER` | Utilisateur MySQL | root |
| `DB_PASSWORD` | Mot de passe MySQL | - |
| `DB_NAME` | Nom de la base de données | face_recognition_db |
| `PORT` | Port du serveur Flask | 5000 |
| `DEBUG` | Mode debug | False |

### API Endpoints

#### `GET /api/health`
Vérification de l'état du serveur
```json
{
  "status": "healthy",
  "message": "Serveur opérationnel",
  "database": "connected"
}
```

#### `POST /api/register`
Inscription d'un nouvel utilisateur
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "face_data": "data:image/jpeg;base64,..."
}
```

#### `POST /api/login`
Connexion par reconnaissance faciale
```json
{
  "face_data": "data:image/jpeg;base64,..."
}
```

#### `GET /api/users`
Liste des utilisateurs (debug)

## 🐛 Dépannage

### Problèmes courants

#### 1. Erreur de connexion MySQL
```bash
# Vérifier que MySQL est en cours d'exécution
sudo systemctl status mysql

# Redémarrer MySQL
sudo systemctl restart mysql
```

#### 2. Erreur de dépendances Python
```bash
# Mettre à jour pip
pip3 install --upgrade pip

# Réinstaller les dépendances
cd backend
pip3 install -r requirements.txt --force-reinstall
```

#### 3. Erreur de caméra
- Vérifiez les permissions de la caméra
- Assurez-vous qu'aucune autre application n'utilise la caméra
- Testez la caméra dans un navigateur web

#### 4. Erreur de reconnaissance faciale
- Assurez-vous d'avoir un bon éclairage
- Placez votre visage bien centré dans le cadre
- Évitez les lunettes de soleil ou les chapeaux

### Logs
Les logs du backend sont affichés dans la console. Pour plus de détails :
```bash
cd backend
python3 app.py --debug
```

## 🔒 Sécurité

- **Mots de passe hachés** : Utilisation de bcrypt
- **Validation des données** : Vérification côté serveur
- **Encodage facial sécurisé** : Stockage des vecteurs d'encodage
- **CORS configuré** : Protection contre les requêtes non autorisées

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📞 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation
- Vérifiez les logs d'erreur

---

**Note** : Cette application nécessite une webcam fonctionnelle pour la reconnaissance faciale. Assurez-vous que votre système supporte l'accès à la caméra.
