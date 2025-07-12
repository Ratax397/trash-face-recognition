// Script pour la page de connexion
let faceCamera = null;
let capturedFaceImage = null;

document.addEventListener('DOMContentLoaded', () => {
    // Éléments du DOM
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    const loginForm = document.getElementById('loginForm');
    const messageDiv = document.getElementById('message');
    const registerLink = document.getElementById('registerLink');
    const faceLoginBtn = document.getElementById('faceLogin');

    // Gestion des onglets
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.dataset.tab;
            
            // Retirer la classe active de tous les onglets et contenus
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Ajouter la classe active à l'onglet cliqué et son contenu
            tab.classList.add('active');
            document.getElementById(`${tabName}-tab`).classList.add('active');
            
            // Réinitialiser la caméra si on change d'onglet
            if (faceCamera) {
                faceCamera.reset();
                capturedFaceImage = null;
                updateFaceLoginButton();
            }
        });
    });

    // Configuration de la caméra pour la reconnaissance faciale
    faceCamera = setupCameraControls(
        'cameraPreview',
        'startCamera',
        'capturePhoto',
        (imageData) => {
            capturedFaceImage = imageData;
            updateFaceLoginButton();
        }
    );

    // Connexion traditionnelle par mot de passe
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const submitBtn = e.target.querySelector('button[type="submit"]');
        
        if (!username || !password) {
            showMessage(messageDiv, 'Veuillez remplir tous les champs.', 'error');
            return;
        }
        
        try {
            setButtonLoading(submitBtn, true);
            
            const response = await api.login({
                username: username,
                password: password
            });
            
            // Sauvegarder l'utilisateur connecté
            storage.setUser(response.user);
            
            showMessage(messageDiv, 'Connexion réussie ! Redirection...', 'success');
            
            // Rediriger vers le tableau de bord après un délai
            setTimeout(() => {
                navigateToPage('dashboard');
            }, 1500);
            
        } catch (error) {
            showMessage(messageDiv, error.message, 'error');
        } finally {
            setButtonLoading(submitBtn, false);
        }
    });

    // Connexion par reconnaissance faciale
    faceLoginBtn.addEventListener('click', async () => {
        const username = document.getElementById('face-username').value;
        
        if (!username) {
            showMessage(messageDiv, 'Veuillez entrer votre nom d\'utilisateur.', 'error');
            return;
        }
        
        if (!capturedFaceImage) {
            showMessage(messageDiv, 'Veuillez d\'abord capturer votre photo.', 'error');
            return;
        }
        
        try {
            setButtonLoading(faceLoginBtn, true);
            
            const response = await api.faceLogin({
                username: username,
                face_image: capturedFaceImage
            });
            
            // Sauvegarder l'utilisateur connecté
            storage.setUser(response.user);
            
            showMessage(messageDiv, response.message, 'success');
            
            // Rediriger vers le tableau de bord après un délai
            setTimeout(() => {
                navigateToPage('dashboard');
            }, 1500);
            
        } catch (error) {
            showMessage(messageDiv, error.message, 'error');
        } finally {
            setButtonLoading(faceLoginBtn, false);
        }
    });

    // Lien vers la page d'inscription
    registerLink.addEventListener('click', (e) => {
        e.preventDefault();
        navigateToPage('register');
    });

    function updateFaceLoginButton() {
        if (capturedFaceImage && document.getElementById('face-username').value) {
            faceLoginBtn.style.display = 'inline-block';
        } else {
            faceLoginBtn.style.display = 'none';
        }
    }

    // Mettre à jour le bouton de connexion faciale quand le nom d'utilisateur change
    document.getElementById('face-username').addEventListener('input', updateFaceLoginButton);

    // Vérifier si l'utilisateur est déjà connecté
    const currentUser = storage.getUser();
    if (currentUser) {
        navigateToPage('dashboard');
    }
});