#!/bin/bash

# Script de démarrage de l'application de reconnaissance faciale
# Electron.js + Python Flask + MySQL

echo "🚀 Démarrage de l'application de reconnaissance faciale"
echo "=================================================="

# Vérifier si Node.js est installé
if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si MySQL est installé et en cours d'exécution
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si MySQL est en cours d'exécution
if ! pgrep -x "mysqld" > /dev/null; then
    echo "⚠️  MySQL ne semble pas être en cours d'exécution."
    echo "   Démarrez MySQL avec: sudo systemctl start mysql"
    exit 1
fi

echo "✅ Vérifications de base terminées"

# Installer les dépendances Node.js si nécessaire
if [ ! -d "node_modules" ]; then
    echo "📦 Installation des dépendances Node.js..."
    npm install
fi

# Installer les dépendances Python si nécessaire
if [ ! -f "backend/.env" ]; then
    echo "📝 Création du fichier de configuration..."
    cp backend/.env.example backend/.env
    echo "⚠️  Veuillez configurer le fichier backend/.env avec vos paramètres MySQL"
fi

# Démarrer le backend Python
echo "🐍 Démarrage du serveur Python..."
cd backend
python3 start_server.py &
BACKEND_PID=$!
cd ..

# Attendre que le backend soit prêt
echo "⏳ Attente du démarrage du backend..."
sleep 5

# Vérifier si le backend est en cours d'exécution
if ! curl -s http://localhost:5000/api/health > /dev/null; then
    echo "❌ Le backend n'a pas démarré correctement"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Backend démarré avec succès"

# Démarrer l'application Electron
echo "⚡ Démarrage de l'application Electron..."
npm start &
ELECTRON_PID=$!

echo "🎉 Application démarrée avec succès!"
echo "📱 Interface Electron: Application desktop"
echo "🌐 Backend API: http://localhost:5000"
echo ""
echo "⏹️  Appuyez sur Ctrl+C pour arrêter l'application"

# Fonction de nettoyage
cleanup() {
    echo ""
    echo "🛑 Arrêt de l'application..."
    kill $BACKEND_PID 2>/dev/null
    kill $ELECTRON_PID 2>/dev/null
    echo "✅ Application arrêtée"
    exit 0
}

# Capturer Ctrl+C
trap cleanup SIGINT

# Attendre que les processus se terminent
wait