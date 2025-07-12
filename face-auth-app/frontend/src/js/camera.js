// Module de gestion de la caméra
class CameraManager {
    constructor() {
        this.stream = null;
        this.video = null;
        this.canvas = null;
        this.capturedImage = null;
    }

    async startCamera(previewElement) {
        try {
            // Demander l'accès à la caméra
            this.stream = await navigator.mediaDevices.getUserMedia({ 
                video: { width: 640, height: 480 } 
            });

            // Créer l'élément vidéo
            this.video = document.createElement('video');
            this.video.srcObject = this.stream;
            this.video.autoplay = true;
            this.video.playsInline = true;

            // Nettoyer le contenu de l'aperçu et ajouter la vidéo
            previewElement.innerHTML = '';
            previewElement.appendChild(this.video);

            return true;
        } catch (error) {
            console.error('Erreur lors de l\'accès à la caméra:', error);
            
            let errorMessage = 'Impossible d\'accéder à la caméra. ';
            if (error.name === 'NotAllowedError') {
                errorMessage += 'Veuillez autoriser l\'accès à la caméra.';
            } else if (error.name === 'NotFoundError') {
                errorMessage += 'Aucune caméra trouvée.';
            } else {
                errorMessage += 'Vérifiez que votre caméra est connectée.';
            }
            
            previewElement.innerHTML = `<span style="color: #e74c3c;">${errorMessage}</span>`;
            return false;
        }
    }

    capturePhoto(previewElement) {
        if (!this.video) {
            console.error('Caméra non initialisée');
            return null;
        }

        // Créer un canvas pour capturer l'image
        this.canvas = document.createElement('canvas');
        const context = this.canvas.getContext('2d');

        // Définir les dimensions du canvas
        this.canvas.width = this.video.videoWidth;
        this.canvas.height = this.video.videoHeight;

        // Dessiner l'image de la vidéo sur le canvas
        context.drawImage(this.video, 0, 0);

        // Convertir en base64
        this.capturedImage = this.canvas.toDataURL('image/jpeg', 0.8);

        // Remplacer la vidéo par l'image capturée
        previewElement.innerHTML = '';
        previewElement.appendChild(this.canvas);

        // Arrêter la caméra
        this.stopCamera();

        return this.capturedImage;
    }

    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        this.video = null;
    }

    getCapturedImage() {
        return this.capturedImage;
    }

    reset() {
        this.stopCamera();
        this.canvas = null;
        this.capturedImage = null;
    }
}

// Fonctions utilitaires pour la gestion de la caméra
function setupCameraControls(
    previewElementId, 
    startButtonId, 
    captureButtonId, 
    onCaptureCallback = null,
    retakeButtonId = null
) {
    const previewElement = document.getElementById(previewElementId);
    const startButton = document.getElementById(startButtonId);
    const captureButton = document.getElementById(captureButtonId);
    const retakeButton = retakeButtonId ? document.getElementById(retakeButtonId) : null;
    
    const camera = new CameraManager();

    // Démarrer la caméra
    startButton.addEventListener('click', async () => {
        setButtonLoading(startButton, true);
        
        const success = await camera.startCamera(previewElement);
        
        setButtonLoading(startButton, false);
        
        if (success) {
            startButton.style.display = 'none';
            captureButton.style.display = 'inline-block';
        }
    });

    // Capturer la photo
    captureButton.addEventListener('click', () => {
        const imageData = camera.capturePhoto(previewElement);
        
        if (imageData) {
            captureButton.style.display = 'none';
            
            if (retakeButton) {
                retakeButton.style.display = 'inline-block';
            }
            
            // Appeler le callback avec l'image capturée
            if (onCaptureCallback) {
                onCaptureCallback(imageData);
            }
        }
    });

    // Reprendre une photo (optionnel)
    if (retakeButton) {
        retakeButton.addEventListener('click', async () => {
            camera.reset();
            retakeButton.style.display = 'none';
            
            // Redémarrer la caméra
            setButtonLoading(startButton, true);
            startButton.style.display = 'inline-block';
            
            const success = await camera.startCamera(previewElement);
            
            setButtonLoading(startButton, false);
            
            if (success) {
                startButton.style.display = 'none';
                captureButton.style.display = 'inline-block';
            }
            
            // Réinitialiser le callback
            if (onCaptureCallback) {
                onCaptureCallback(null);
            }
        });
    }

    return camera;
}