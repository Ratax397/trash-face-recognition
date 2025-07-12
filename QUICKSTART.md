# 🚀 Guide de Démarrage Rapide

Ce guide vous permettra de démarrer l'application de reconnaissance faciale en quelques minutes.

## ⚡ Installation Express

### 1. Prérequis
Assurez-vous d'avoir installé :
- **Node.js** (v16+) : https://nodejs.org/
- **Python 3.8+** : https://python.org/
- **MySQL 8.0+** : https://dev.mysql.com/

### 2. Installation automatique
```bash
# Cloner le projet
git clone <repository-url>
cd face-recognition-app

# Tester la configuration
python3 test_setup.py

# Si tout est OK, démarrer l'application
./start.sh
```

## 🔧 Configuration Manuelle

### 1. Base de données MySQL
```bash
# Démarrer MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# Créer la base de données
sudo mysql -u root -p
```

Dans MySQL :
```sql
CREATE DATABASE face_recognition_db;
CREATE USER 'face_user'@'localhost' IDENTIFIED BY 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON face_recognition_db.* TO 'face_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 2. Configuration de l'environnement
```bash
# Copier le fichier de configuration
cp backend/.env.example backend/.env

# Éditer la configuration
nano backend/.env
```

Modifier le fichier `.env` :
```env
DB_HOST=localhost
DB_USER=face_user
DB_PASSWORD=votre_mot_de_passe
DB_NAME=face_recognition_db
PORT=5000
DEBUG=False
```

### 3. Installation des dépendances
```bash
# Dépendances Node.js
npm install

# Dépendances Python
cd backend
pip3 install -r requirements.txt
cd ..
```

## 🎯 Utilisation

### Inscription
1. Lancez l'application : `./start.sh`
2. Cliquez sur "Inscription"
3. Remplissez le formulaire
4. Cliquez sur "Démarrer la caméra"
5. Placez votre visage dans le cadre
6. Cliquez sur "Capturer le visage"
7. Cliquez sur "S'inscrire"

### Connexion
1. Cliquez sur "Connexion"
2. Cliquez sur "Démarrer la caméra"
3. Placez votre visage dans le cadre
4. Cliquez sur "Reconnaître le visage"

## 🐛 Problèmes Courants

### Erreur MySQL
```bash
sudo systemctl status mysql
sudo systemctl restart mysql
```

### Erreur de caméra
- Vérifiez les permissions
- Fermez les autres applications utilisant la caméra
- Testez dans un navigateur web

### Erreur de dépendances Python
```bash
pip3 install --upgrade pip
cd backend
pip3 install -r requirements.txt --force-reinstall
```

## 📞 Support

- **Test de configuration** : `python3 test_setup.py`
- **Logs du backend** : Vérifiez la console
- **Documentation complète** : `README.md`

---

**Note** : Assurez-vous d'avoir une webcam fonctionnelle pour utiliser la reconnaissance faciale.