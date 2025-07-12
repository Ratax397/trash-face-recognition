#!/usr/bin/env python3
"""
Script de démarrage du serveur Flask
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """Vérifier que toutes les dépendances sont installées"""
    required_packages = [
        'flask',
        'flask-cors',
        'mysql-connector-python',
        'face-recognition',
        'opencv-python',
        'numpy',
        'Pillow',
        'bcrypt',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Dépendances manquantes:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installation des dépendances...")
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ Dépendances installées avec succès")
        except subprocess.CalledProcessError:
            print("❌ Erreur lors de l'installation des dépendances")
            return False
    
    return True

def check_mysql_connection():
    """Vérifier la connexion à MySQL"""
    try:
        import mysql.connector
        from dotenv import load_dotenv
        
        load_dotenv()
        
        config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'face_recognition_db')
        }
        
        # Essayer de se connecter
        connection = mysql.connector.connect(**config)
        connection.close()
        print("✅ Connexion à MySQL établie")
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion à MySQL: {e}")
        print("\n📋 Vérifiez votre configuration:")
        print("   1. MySQL est-il installé et en cours d'exécution?")
        print("   2. Avez-vous créé la base de données?")
        print("   3. Vérifiez le fichier .env")
        return False

def create_database():
    """Créer la base de données si elle n'existe pas"""
    try:
        import mysql.connector
        from dotenv import load_dotenv
        
        load_dotenv()
        
        config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
        }
        
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        db_name = os.getenv('DB_NAME', 'face_recognition_db')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        
        connection.close()
        print(f"✅ Base de données '{db_name}' créée/vérifiée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de la base de données: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Démarrage du serveur de reconnaissance faciale")
    print("=" * 50)
    
    # Vérifier les dépendances
    if not check_dependencies():
        return
    
    # Créer la base de données
    if not create_database():
        return
    
    # Vérifier la connexion MySQL
    if not check_mysql_connection():
        return
    
    print("\n✅ Toutes les vérifications sont passées")
    print("🌐 Démarrage du serveur Flask...")
    print("=" * 50)
    
    # Démarrer le serveur
    try:
        from app import app
        
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('DEBUG', 'False').lower() == 'true'
        
        print(f"📡 Serveur accessible sur: http://localhost:{port}")
        print(f"🔧 Mode debug: {'Activé' if debug else 'Désactivé'}")
        print("\n⏹️  Appuyez sur Ctrl+C pour arrêter le serveur")
        
        app.run(host='0.0.0.0', port=port, debug=debug)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Serveur arrêté par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du démarrage du serveur: {e}")

if __name__ == '__main__':
    main()