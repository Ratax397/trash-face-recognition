from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import cv2
import numpy as np
import face_recognition
import mysql.connector
from mysql.connector import Error
import bcrypt
from datetime import datetime
import logging
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration de la base de données
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'face_recognition_db'),
    'charset': 'utf8mb4'
}

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Établir la connexion à la base de données"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            logger.info("Connexion à la base de données établie")
        except Error as e:
            logger.error(f"Erreur de connexion à la base de données: {e}")
            raise
    
    def create_tables(self):
        """Créer les tables nécessaires"""
        try:
            cursor = self.connection.cursor()
            
            # Table des utilisateurs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            
            # Table des encodages faciaux
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS face_encodings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    face_encoding LONGTEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            
            self.connection.commit()
            logger.info("Tables créées avec succès")
            
        except Error as e:
            logger.error(f"Erreur lors de la création des tables: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
    
    def get_connection(self):
        """Obtenir une connexion active"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection

# Instance globale du gestionnaire de base de données
db_manager = DatabaseManager()

class FaceRecognitionService:
    @staticmethod
    def encode_face_from_base64(base64_image):
        """Encoder un visage à partir d'une image base64"""
        try:
            # Décoder l'image base64
            image_data = base64.b64decode(base64_image.split(',')[1])
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Convertir BGR vers RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Détecter les visages
            face_locations = face_recognition.face_locations(rgb_image)
            
            if not face_locations:
                raise ValueError("Aucun visage détecté dans l'image")
            
            if len(face_locations) > 1:
                raise ValueError("Plusieurs visages détectés. Veuillez ne capturer qu'un seul visage.")
            
            # Encoder le visage
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
            
            if not face_encodings:
                raise ValueError("Impossible d'encoder le visage détecté")
            
            return face_encodings[0]
            
        except Exception as e:
            logger.error(f"Erreur lors de l'encodage du visage: {e}")
            raise
    
    @staticmethod
    def compare_faces(known_encoding, face_encoding, tolerance=0.6):
        """Comparer deux encodages faciaux"""
        try:
            # Convertir les encodages en listes si nécessaire
            if isinstance(known_encoding, str):
                known_encoding = np.array(eval(known_encoding))
            if isinstance(face_encoding, str):
                face_encoding = np.array(eval(face_encoding))
            
            # Comparer les visages
            matches = face_recognition.compare_faces([known_encoding], face_encoding, tolerance=tolerance)
            return matches[0] if matches else False
            
        except Exception as e:
            logger.error(f"Erreur lors de la comparaison des visages: {e}")
            return False

# Routes API
@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérification de l'état du serveur"""
    try:
        db_manager.get_connection()
        return jsonify({
            'status': 'healthy',
            'message': 'Serveur opérationnel',
            'database': 'connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': str(e),
            'database': 'disconnected'
        }), 500

@app.route('/api/register', methods=['POST'])
def register():
    """Inscription d'un nouvel utilisateur"""
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['username', 'email', 'password', 'face_data']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Le champ {field} est requis'}), 400
        
        username = data['username'].strip()
        email = data['email'].strip()
        password = data['password']
        face_data = data['face_data']
        
        # Validation de la longueur du mot de passe
        if len(password) < 6:
            return jsonify({'error': 'Le mot de passe doit contenir au moins 6 caractères'}), 400
        
        # Encoder le visage
        try:
            face_encoding = FaceRecognitionService.encode_face_from_base64(face_data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        # Hasher le mot de passe
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Insérer dans la base de données
        connection = db_manager.get_connection()
        cursor = connection.cursor()
        
        try:
            # Insérer l'utilisateur
            cursor.execute("""
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
            """, (username, email, password_hash.decode('utf-8')))
            
            user_id = cursor.lastrowid
            
            # Insérer l'encodage facial
            cursor.execute("""
                INSERT INTO face_encodings (user_id, face_encoding)
                VALUES (%s, %s)
            """, (user_id, str(face_encoding.tolist())))
            
            connection.commit()
            
            logger.info(f"Utilisateur {username} inscrit avec succès")
            
            return jsonify({
                'message': 'Inscription réussie',
                'user_id': user_id,
                'username': username
            }), 201
            
        except mysql.connector.IntegrityError as e:
            if "Duplicate entry" in str(e):
                if "username" in str(e):
                    return jsonify({'error': 'Ce nom d\'utilisateur existe déjà'}), 409
                elif "email" in str(e):
                    return jsonify({'error': 'Cet email existe déjà'}), 409
            return jsonify({'error': 'Erreur lors de l\'inscription'}), 500
        finally:
            cursor.close()
            
    except Exception as e:
        logger.error(f"Erreur lors de l'inscription: {e}")
        return jsonify({'error': 'Erreur interne du serveur'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Connexion par reconnaissance faciale"""
    try:
        data = request.get_json()
        
        if 'face_data' not in data or not data['face_data']:
            return jsonify({'error': 'Les données faciales sont requises'}), 400
        
        face_data = data['face_data']
        
        # Encoder le visage fourni
        try:
            face_encoding = FaceRecognitionService.encode_face_from_base64(face_data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        # Récupérer tous les utilisateurs et leurs encodages
        connection = db_manager.get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("""
                SELECT u.id, u.username, fe.face_encoding
                FROM users u
                JOIN face_encodings fe ON u.id = fe.user_id
            """)
            
            users = cursor.fetchall()
            
            if not users:
                return jsonify({'error': 'Aucun utilisateur enregistré'}), 404
            
            # Comparer avec tous les utilisateurs
            for user_id, username, stored_encoding in users:
                if FaceRecognitionService.compare_faces(stored_encoding, face_encoding):
                    logger.info(f"Connexion réussie pour l'utilisateur {username}")
                    return jsonify({
                        'message': 'Connexion réussie',
                        'user_id': user_id,
                        'username': username
                    }), 200
            
            return jsonify({'error': 'Visage non reconnu'}), 401
            
        finally:
            cursor.close()
            
    except Exception as e:
        logger.error(f"Erreur lors de la connexion: {e}")
        return jsonify({'error': 'Erreur interne du serveur'}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """Récupérer la liste des utilisateurs (pour debug)"""
    try:
        connection = db_manager.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT id, username, email, created_at
            FROM users
            ORDER BY created_at DESC
        """)
        
        users = cursor.fetchall()
        
        # Convertir les dates en string pour la sérialisation JSON
        for user in users:
            user['created_at'] = user['created_at'].isoformat()
        
        return jsonify({'users': users}), 200
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des utilisateurs: {e}")
        return jsonify({'error': 'Erreur interne du serveur'}), 500
    finally:
        cursor.close()

if __name__ == '__main__':
    # Configuration du serveur
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Démarrage du serveur sur le port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)