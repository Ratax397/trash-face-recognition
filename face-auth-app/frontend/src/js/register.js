// Script pour la page d'inscription
let registerCamera = null;
let capturedRegisterImage = null;

document.addEventListener('DOMContentLoaded', () => {
    // Éléments du DOM
    const registerForm = document.getElementById('registerForm');
    const messageDiv = document.getElementById('registerMessage');
    const loginLink = document.getElementById('loginLink');
    const registerBtn = document.getElementById('registerBtn');

    // Configuration de la caméra pour l'inscription
    registerCamera = setupCameraControls(
        'registerCameraPreview',
        'startRegisterCamera',
        'captureRegisterPhoto',
        (imageData) => {
            capturedRegisterImage = imageData;
            updateRegisterButton();
        },
        'retakePhoto'
    );

    // Gestion du formulaire d'inscription
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const username = formData.get('username');
        const email = formData.get('email');
        const password = formData.get('password');
        const confirmPassword = formData.get('confirmPassword');
        
        // Validation des champs
        if (!username || !email || !password || !confirmPassword) {
            showMessage(messageDiv, 'Veuillez remplir tous les champs.', 'error');
            return;
        }
        
        if (password !== confirmPassword) {
            showMessage(messageDiv, 'Les mots de passe ne correspondent pas.', 'error');
            return;
        }
        
        if (password.length < 6) {
            showMessage(messageDiv, 'Le mot de passe doit contenir au moins 6 caractères.', 'error');
            return;
        }
        
        if (!capturedRegisterImage) {
            showMessage(messageDiv, 'Veuillez capturer votre photo pour la reconnaissance faciale.', 'error');
            return;
        }
        
        // Validation de l'email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            showMessage(messageDiv, 'Veuillez entrer une adresse email valide.', 'error');
            return;
        }
        
        try {
            setButtonLoading(registerBtn, true);
            
            const userData = {
                username: username,
                email: email,
                password: password,
                face_image: capturedRegisterImage
            };
            
            const response = await api.register(userData);
            
            showMessage(messageDiv, 'Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success');
            
            // Rediriger vers la page de connexion après un délai
            setTimeout(() => {
                navigateToPage('login');
            }, 2000);
            
        } catch (error) {
            showMessage(messageDiv, error.message, 'error');
        } finally {
            setButtonLoading(registerBtn, false);
        }
    });

    // Lien vers la page de connexion
    loginLink.addEventListener('click', (e) => {
        e.preventDefault();
        navigateToPage('login');
    });

    // Validation en temps réel des mots de passe
    const passwordField = document.getElementById('reg-password');
    const confirmPasswordField = document.getElementById('reg-confirm-password');
    
    function validatePasswords() {
        const password = passwordField.value;
        const confirmPassword = confirmPasswordField.value;
        
        if (confirmPassword && password !== confirmPassword) {
            confirmPasswordField.setCustomValidity('Les mots de passe ne correspondent pas');
        } else {
            confirmPasswordField.setCustomValidity('');
        }
        
        updateRegisterButton();
    }
    
    passwordField.addEventListener('input', validatePasswords);
    confirmPasswordField.addEventListener('input', validatePasswords);

    // Validation en temps réel des autres champs
    const usernameField = document.getElementById('reg-username');
    const emailField = document.getElementById('reg-email');
    
    [usernameField, emailField].forEach(field => {
        field.addEventListener('input', updateRegisterButton);
    });

    function updateRegisterButton() {
        const username = usernameField.value.trim();
        const email = emailField.value.trim();
        const password = passwordField.value;
        const confirmPassword = confirmPasswordField.value;
        
        const isFormValid = username && 
                          email && 
                          password && 
                          confirmPassword && 
                          password === confirmPassword && 
                          password.length >= 6 &&
                          capturedRegisterImage;
        
        registerBtn.disabled = !isFormValid;
    }

    // Vérifier si l'utilisateur est déjà connecté
    const currentUser = storage.getUser();
    if (currentUser) {
        navigateToPage('dashboard');
    }
});