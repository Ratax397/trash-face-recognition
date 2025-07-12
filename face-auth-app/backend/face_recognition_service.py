import cv2
import face_recognition
import numpy as np
import pickle
import base64
from io import BytesIO
from PIL import Image

class FaceRecognitionService:
    
    @staticmethod
    def encode_face_from_base64(image_base64: str):
        """
        Encode un visage à partir d'une image en base64
        """
        try:
            # Décoder l'image base64
            image_data = base64.b64decode(image_base64.split(',')[1] if ',' in image_base64 else image_base64)
            image = Image.open(BytesIO(image_data))
            
            # Convertir en array numpy
            img_array = np.array(image)
            
            # Convertir RGB vers BGR pour OpenCV
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # Encoder le visage
            face_encodings = face_recognition.face_encodings(img_array)
            
            if len(face_encodings) > 0:
                return face_encodings[0]
            else:
                return None
                
        except Exception as e:
            print(f"Erreur lors de l'encodage: {e}")
            return None
    
    @staticmethod
    def verify_face(known_face_encoding, image_base64: str, tolerance=0.6):
        """
        Vérifie si le visage dans l'image correspond à l'encodage connu
        """
        try:
            current_face_encoding = FaceRecognitionService.encode_face_from_base64(image_base64)
            
            if current_face_encoding is None:
                return False, "Aucun visage détecté dans l'image"
            
            # Désérialiser l'encodage connu s'il est en bytes
            if isinstance(known_face_encoding, bytes):
                known_face_encoding = pickle.loads(known_face_encoding)
            
            # Comparer les visages
            matches = face_recognition.compare_faces([known_face_encoding], current_face_encoding, tolerance=tolerance)
            face_distance = face_recognition.face_distance([known_face_encoding], current_face_encoding)[0]
            
            if matches[0]:
                confidence = 1 - face_distance
                return True, f"Visage reconnu avec {confidence:.2%} de confiance"
            else:
                return False, f"Visage non reconnu (distance: {face_distance:.2f})"
                
        except Exception as e:
            print(f"Erreur lors de la vérification: {e}")
            return False, f"Erreur lors de la vérification: {str(e)}"
    
    @staticmethod
    def serialize_encoding(face_encoding):
        """
        Sérialise un encodage de visage pour le stockage en base de données
        """
        return pickle.dumps(face_encoding)
    
    @staticmethod
    def deserialize_encoding(serialized_encoding):
        """
        Désérialise un encodage de visage depuis la base de données
        """
        return pickle.loads(serialized_encoding)