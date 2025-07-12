// Variables globales
let loginStream = null;
let registerStream = null;
let capturedFaceData = null;
const API_BASE_URL = 'http://localhost:5000/api';

// Éléments DOM
const elements = {
    // Onglets
    loginTab: document.getElementById('login'),
    registerTab: document.getElementById('register'),
    
    // Caméra de connexion
    loginVideo: document.getElementById('loginVideo'),
    loginCanvas: document.getElementById('loginCanvas'),
    startLoginCamera: document.getElementById('startLoginCamera'),
    loginFace: document.getElementById('loginFace'),
    loginStatus: document.getElementById('loginStatus'),
    
    // Caméra d'inscription
    registerVideo: document.getElementById('registerVideo'),
    registerCanvas: document.getElementById('registerCanvas'),
    startRegisterCamera: document.getElementById('startRegisterCamera'),
    captureFace: document.getElementById('captureFace'),
    
    // Formulaire d'inscription
    registerForm: document.getElementById('registerForm'),
    registerBtn: document.getElementById('registerBtn'),
    registerStatus: document.getElementById('registerStatus'),
    
    // Champs du formulaire
    username: document.getElementById('username'),
    email: document.getElementById('email'),
    password: document.getElementById('password'),
    confirmPassword: document.getElementById('confirmPassword')
};

// Gestion des onglets
function showTab(tabName) {
    // Masquer tous les onglets
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Afficher l'onglet sélectionné
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    
    // Arrêter les flux vidéo lors du changement d'onglet
    stopAllCameras();
}

// Gestion de la caméra
async function startCamera(videoElement) {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 640 },
                height: { ideal: 480 },
                facingMode: 'user'
            }
        });
        
        videoElement.srcObject = stream;
        return stream;
    } catch (error) {
        console.error('Erreur lors du démarrage de la caméra:', error);
        showStatus('error', 'Impossible d\'accéder à la caméra. Vérifiez les permissions.');
        return null;
    }
}

function stopCamera(stream) {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
}

function stopAllCameras() {
    stopCamera(loginStream);
    stopCamera(registerStream);
    loginStream = null;
    registerStream = null;
}

// Capture d'image depuis la vidéo
function captureImage(videoElement, canvasElement) {
    const context = canvasElement.getContext('2d');
    canvasElement.width = videoElement.videoWidth;
    canvasElement.height = videoElement.videoHeight;
    context.drawImage(videoElement, 0, 0);
    
    return canvasElement.toDataURL('image/jpeg', 0.8);
}

// Affichage des messages de statut
function showStatus(element, type, message) {
    element.className = `status-message ${type}`;
    element.innerHTML = message;
}

function showLoadingStatus(element, message) {
    element.className = 'status-message info';
    element.innerHTML = `<div class="loading"></div>${message}`;
}

// Validation du formulaire
function validateForm() {
    const username = elements.username.value.trim();
    const email = elements.email.value.trim();
    const password = elements.password.value;
    const confirmPassword = elements.confirmPassword.value;
    
    if (!username || !email || !password || !confirmPassword) {
        return false;
    }
    
    if (password !== confirmPassword) {
        showStatus(elements.registerStatus, 'error', 'Les mots de passe ne correspondent pas');
        return false;
    }
    
    if (password.length < 6) {
        showStatus(elements.registerStatus, 'error', 'Le mot de passe doit contenir au moins 6 caractères');
        return false;
    }
    
    if (!capturedFaceData) {
        showStatus(elements.registerStatus, 'error', 'Veuillez capturer votre visage');
        return false;
    }
    
    return true;
}

// API calls
async function registerUser(userData) {
    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Erreur lors de l\'inscription');
        }
        
        return data;
    } catch (error) {
        console.error('Erreur API:', error);
        throw error;
    }
}

async function loginWithFace(faceData) {
    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ face_data: faceData })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Erreur lors de la connexion');
        }
        
        return data;
    } catch (error) {
        console.error('Erreur API:', error);
        throw error;
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Caméra de connexion
    elements.startLoginCamera.addEventListener('click', async () => {
        showLoadingStatus(elements.loginStatus, 'Démarrage de la caméra...');
        
        loginStream = await startCamera(elements.loginVideo);
        
        if (loginStream) {
            elements.loginFace.disabled = false;
            showStatus(elements.loginStatus, 'success', 'Caméra démarrée. Placez votre visage dans le cadre.');
        }
    });
    
    elements.loginFace.addEventListener('click', async () => {
        if (!loginStream) return;
        
        showLoadingStatus(elements.loginStatus, 'Reconnaissance en cours...');
        
        try {
            const faceData = captureImage(elements.loginVideo, elements.loginCanvas);
            const result = await loginWithFace(faceData);
            
            showStatus(elements.loginStatus, 'success', `Connexion réussie ! Bienvenue ${result.username}`);
            
            // Arrêter la caméra après connexion réussie
            setTimeout(() => {
                stopCamera(loginStream);
                loginStream = null;
                elements.loginFace.disabled = true;
            }, 2000);
            
        } catch (error) {
            showStatus(elements.loginStatus, 'error', error.message);
        }
    });
    
    // Caméra d'inscription
    elements.startRegisterCamera.addEventListener('click', async () => {
        showLoadingStatus(elements.registerStatus, 'Démarrage de la caméra...');
        
        registerStream = await startCamera(elements.registerVideo);
        
        if (registerStream) {
            elements.captureFace.disabled = false;
            showStatus(elements.registerStatus, 'success', 'Caméra démarrée. Placez votre visage dans le cadre et cliquez sur "Capturer le visage".');
        }
    });
    
    elements.captureFace.addEventListener('click', () => {
        if (!registerStream) return;
        
        capturedFaceData = captureImage(elements.registerVideo, elements.registerCanvas);
        elements.registerBtn.disabled = false;
        
        showStatus(elements.registerStatus, 'success', 'Visage capturé avec succès ! Vous pouvez maintenant vous inscrire.');
        
        // Arrêter la caméra après capture
        stopCamera(registerStream);
        registerStream = null;
        elements.captureFace.disabled = true;
    });
    
    // Formulaire d'inscription
    elements.registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }
        
        showLoadingStatus(elements.registerStatus, 'Inscription en cours...');
        
        try {
            const userData = {
                username: elements.username.value.trim(),
                email: elements.email.value.trim(),
                password: elements.password.value,
                face_data: capturedFaceData
            };
            
            const result = await registerUser(userData);
            
            showStatus(elements.registerStatus, 'success', 'Inscription réussie ! Vous pouvez maintenant vous connecter avec la reconnaissance faciale.');
            
            // Réinitialiser le formulaire
            elements.registerForm.reset();
            capturedFaceData = null;
            elements.registerBtn.disabled = true;
            
        } catch (error) {
            showStatus(elements.registerStatus, 'error', error.message);
        }
    });
    
    // Validation en temps réel
    elements.password.addEventListener('input', () => {
        if (elements.password.value !== elements.confirmPassword.value) {
            elements.confirmPassword.style.borderColor = '#dc3545';
        } else {
            elements.confirmPassword.style.borderColor = '#28a745';
        }
    });
    
    elements.confirmPassword.addEventListener('input', () => {
        if (elements.password.value !== elements.confirmPassword.value) {
            elements.confirmPassword.style.borderColor = '#dc3545';
        } else {
            elements.confirmPassword.style.borderColor = '#28a745';
        }
    });
});

// Gestion de la fermeture de l'application
window.addEventListener('beforeunload', () => {
    stopAllCameras();
});

// Gestion des erreurs globales
window.addEventListener('error', (event) => {
    console.error('Erreur JavaScript:', event.error);
});

// Test de connexion au backend
async function testBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('Backend connecté avec succès');
        } else {
            console.warn('Backend non disponible');
        }
    } catch (error) {
        console.warn('Impossible de se connecter au backend:', error.message);
    }
}

// Tester la connexion au démarrage
setTimeout(testBackendConnection, 1000);