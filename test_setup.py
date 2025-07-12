#!/usr/bin/env python3
"""
Script de test pour vérifier l'installation et la configuration
"""

import sys
import subprocess
import importlib
import os
from pathlib import Path

def check_python_version():
    """Vérifier la version de Python"""
    print("🐍 Vérification de la version Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Version 3.8+ requise")
        return False

def check_nodejs():
    """Vérifier que Node.js est installé"""
    print("\n📦 Vérification de Node.js...")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js {version} - OK")
            return True
        else:
            print("❌ Node.js non trouvé")
            return False
    except FileNotFoundError:
        print("❌ Node.js non installé")
        return False

def check_npm():
    """Vérifier que npm est installé"""
    print("\n📦 Vérification de npm...")
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ npm {version} - OK")
            return True
        else:
            print("❌ npm non trouvé")
            return False
    except FileNotFoundError:
        print("❌ npm non installé")
        return False

def check_mysql():
    """Vérifier que MySQL est installé et en cours d'exécution"""
    print("\n🗄️ Vérification de MySQL...")
    try:
        result = subprocess.run(['mysql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ MySQL installé: {version}")
            
            # Vérifier si MySQL est en cours d'exécution
            result = subprocess.run(['systemctl', 'is-active', 'mysql'], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip() == 'active':
                print("✅ MySQL en cours d'exécution")
                return True
            else:
                print("⚠️ MySQL installé mais pas en cours d'exécution")
                print("   Démarrez avec: sudo systemctl start mysql")
                return False
        else:
            print("❌ MySQL non trouvé")
            return False
    except FileNotFoundError:
        print("❌ MySQL non installé")
        return False

def check_python_packages():
    """Vérifier les packages Python requis"""
    print("\n🐍 Vérification des packages Python...")
    required_packages = [
        'flask',
        'flask_cors',
        'mysql.connector',
        'face_recognition',
        'cv2',
        'numpy',
        'PIL',
        'bcrypt',
        'dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                importlib.import_module('cv2')
            elif package == 'PIL':
                importlib.import_module('PIL')
            else:
                importlib.import_module(package)
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - Manquant")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Packages manquants: {', '.join(missing_packages)}")
        print("   Installez avec: pip3 install -r backend/requirements.txt")
        return False
    
    return True

def check_files():
    """Vérifier que tous les fichiers nécessaires existent"""
    print("\n📁 Vérification des fichiers...")
    required_files = [
        'main.js',
        'index.html',
        'styles.css',
        'renderer.js',
        'package.json',
        'start.sh',
        'backend/app.py',
        'backend/requirements.txt',
        'backend/start_server.py',
        'backend/.env.example'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} - OK")
        else:
            print(f"❌ {file_path} - Manquant")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n📁 Fichiers manquants: {', '.join(missing_files)}")
        return False
    
    return True

def check_env_file():
    """Vérifier la configuration de l'environnement"""
    print("\n⚙️ Vérification de la configuration...")
    env_file = Path('backend/.env')
    
    if env_file.exists():
        print("✅ Fichier .env trouvé")
        
        # Vérifier les variables importantes
        with open(env_file, 'r') as f:
            content = f.read()
            
        required_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
        missing_vars = []
        
        for var in required_vars:
            if f'{var}=' in content:
                print(f"✅ {var} - Configuré")
            else:
                print(f"❌ {var} - Manquant")
                missing_vars.append(var)
        
        if missing_vars:
            print(f"\n⚠️ Variables manquantes: {', '.join(missing_vars)}")
            print("   Configurez le fichier backend/.env")
            return False
        
        return True
    else:
        print("❌ Fichier .env manquant")
        print("   Copiez backend/.env.example vers backend/.env et configurez-le")
        return False

def test_database_connection():
    """Tester la connexion à la base de données"""
    print("\n🗄️ Test de connexion à la base de données...")
    try:
        from dotenv import load_dotenv
        import mysql.connector
        
        load_dotenv('backend/.env')
        
        config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'face_recognition_db')
        }
        
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Tester une requête simple
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result and result[0] == 1:
            print("✅ Connexion à la base de données réussie")
            cursor.close()
            connection.close()
            return True
        else:
            print("❌ Erreur lors du test de la base de données")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 Test de configuration de l'application de reconnaissance faciale")
    print("=" * 70)
    
    tests = [
        ("Version Python", check_python_version),
        ("Node.js", check_nodejs),
        ("npm", check_npm),
        ("MySQL", check_mysql),
        ("Packages Python", check_python_packages),
        ("Fichiers", check_files),
        ("Configuration", check_env_file),
        ("Base de données", test_database_connection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nRésultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 Tous les tests sont passés ! L'application est prête à être utilisée.")
        print("   Démarrez avec: ./start.sh")
    else:
        print(f"\n⚠️ {total - passed} problème(s) détecté(s).")
        print("   Consultez les messages ci-dessus pour résoudre les problèmes.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)