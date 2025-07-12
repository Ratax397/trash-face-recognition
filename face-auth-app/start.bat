@echo off
echo 🚀 Démarrage de Face Auth App...

REM Vérifier les prérequis
echo [INFO] Vérification des prérequis...

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python n'est pas installé ou non accessible
    pause
    exit /b 1
)

REM Vérifier Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js n'est pas installé ou non accessible
    pause
    exit /b 1
)

REM Vérifier MySQL
mysql --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] MySQL n'est pas installé ou non accessible
    pause
    exit /b 1
)

echo [INFO] Tous les prérequis sont satisfaits ✓

REM Configuration de la base de données
echo [INFO] Configuration de la base de données...
mysql -u root -e "CREATE DATABASE IF NOT EXISTS face_auth_db;" 2>nul
if errorlevel 1 (
    echo [WARNING] Impossible de créer la base de données automatiquement
    echo [INFO] Veuillez créer manuellement la base de données 'face_auth_db'
) else (
    echo [INFO] Base de données configurée ✓
)

REM Démarrer le backend
echo [INFO] Démarrage du backend Python...
cd backend

REM Vérifier si l'environnement virtuel existe
if not exist "venv" (
    echo [INFO] Création de l'environnement virtuel Python...
    python -m venv venv
    
    echo [INFO] Installation des dépendances...
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

REM Démarrer le serveur en arrière-plan
echo [INFO] Lancement du serveur API...
start /B python main.py

REM Attendre que le serveur soit prêt
echo [INFO] Attente du démarrage du serveur...
timeout /t 5 /nobreak >nul

cd ..

REM Démarrer le frontend
echo [INFO] Démarrage de l'application Electron...
cd frontend

REM Vérifier si les dépendances sont installées
if not exist "node_modules" (
    echo [INFO] Installation des dépendances Node.js...
    npm install
)

REM Démarrer l'application Electron
echo [INFO] Lancement de l'interface utilisateur...
npm start

cd ..

echo [INFO] Application fermée
pause