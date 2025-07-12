#!/bin/bash

# Script de démarrage automatique pour Face Auth App
echo "🚀 Démarrage de Face Auth App..."

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages colorés
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier si MySQL est en cours d'exécution
check_mysql() {
    print_status "Vérification de MySQL..."
    if ! pgrep -x "mysqld" > /dev/null; then
        print_warning "MySQL n'est pas en cours d'exécution."
        print_status "Tentative de démarrage de MySQL..."
        
        # Essayer différentes commandes selon le système
        if command -v systemctl &> /dev/null; then
            sudo systemctl start mysql
        elif command -v brew &> /dev/null; then
            brew services start mysql
        else
            print_error "Impossible de démarrer MySQL automatiquement. Veuillez le démarrer manuellement."
            exit 1
        fi
        
        # Attendre que MySQL soit prêt
        sleep 3
    fi
    print_status "MySQL est en cours d'exécution ✓"
}

# Créer la base de données si elle n'existe pas
setup_database() {
    print_status "Configuration de la base de données..."
    
    if mysql -u root -e "USE face_auth_db;" 2>/dev/null; then
        print_status "Base de données déjà configurée ✓"
    else
        print_status "Création de la base de données..."
        mysql -u root < database/init.sql
        print_status "Base de données créée ✓"
    fi
}

# Démarrer le backend
start_backend() {
    print_status "Démarrage du backend Python..."
    
    cd backend
    
    # Vérifier si l'environnement virtuel existe
    if [ ! -d "venv" ]; then
        print_status "Création de l'environnement virtuel Python..."
        python3 -m venv venv
        
        print_status "Installation des dépendances..."
        source venv/bin/activate
        pip install -r requirements.txt
    else
        source venv/bin/activate
    fi
    
    # Démarrer le serveur en arrière-plan
    print_status "Lancement du serveur API..."
    python main.py &
    BACKEND_PID=$!
    
    # Attendre que le serveur soit prêt
    print_status "Attente du démarrage du serveur..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/ > /dev/null 2>&1; then
            print_status "Serveur API démarré ✓ (PID: $BACKEND_PID)"
            break
        fi
        sleep 1
    done
    
    cd ..
}

# Démarrer le frontend
start_frontend() {
    print_status "Démarrage de l'application Electron..."
    
    cd frontend
    
    # Vérifier si les dépendances sont installées
    if [ ! -d "node_modules" ]; then
        print_status "Installation des dépendances Node.js..."
        npm install
    fi
    
    # Démarrer l'application Electron
    print_status "Lancement de l'interface utilisateur..."
    npm start &
    FRONTEND_PID=$!
    
    cd ..
}

# Fonction de nettoyage
cleanup() {
    print_status "Arrêt de l'application..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        print_status "Backend arrêté"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        print_status "Frontend arrêté"
    fi
    
    exit 0
}

# Gérer l'interruption du script
trap cleanup SIGINT SIGTERM

# Vérifications préliminaires
print_status "Vérification des prérequis..."

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 n'est pas installé"
    exit 1
fi

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js n'est pas installé"
    exit 1
fi

# Vérifier MySQL
if ! command -v mysql &> /dev/null; then
    print_error "MySQL n'est pas installé"
    exit 1
fi

# Démarrage de l'application
check_mysql
setup_database
start_backend
start_frontend

print_status "🎉 Face Auth App démarrée avec succès !"
print_status "Interface utilisateur : Application Electron"
print_status "API Backend : http://localhost:8000"
print_status "Documentation API : http://localhost:8000/docs"
print_status ""
print_status "Appuyez sur Ctrl+C pour arrêter l'application"

# Attendre que l'utilisateur arrête l'application
wait