// Script pour le tableau de bord
document.addEventListener('DOMContentLoaded', () => {
    // Éléments du DOM
    const userNameElement = document.getElementById('userName');
    const userEmailElement = document.getElementById('userEmail');
    const userInitialsElement = document.getElementById('userInitials');
    const memberSinceElement = document.getElementById('memberSince');
    const lastLoginElement = document.getElementById('lastLogin');
    const logoutBtn = document.getElementById('logoutBtn');

    // Vérifier si l'utilisateur est connecté
    const currentUser = storage.getUser();
    if (!currentUser) {
        navigateToPage('login');
        return;
    }

    // Afficher les informations de l'utilisateur
    displayUserInfo(currentUser);

    // Gestion de la déconnexion
    logoutBtn.addEventListener('click', () => {
        // Supprimer les données utilisateur du stockage local
        storage.removeUser();
        
        // Rediriger vers la page de connexion
        navigateToPage('login');
    });

    function displayUserInfo(user) {
        // Nom d'utilisateur
        userNameElement.textContent = user.username;
        
        // Email
        userEmailElement.textContent = user.email;
        
        // Initiales pour l'avatar
        const initials = user.username.charAt(0).toUpperCase();
        userInitialsElement.textContent = initials;
        
        // Date de création du compte
        const createdDate = new Date(user.created_at);
        memberSinceElement.textContent = formatDate(createdDate);
        
        // Dernière connexion (utiliser la date actuelle si pas disponible)
        const lastLoginDate = user.last_login ? new Date(user.last_login) : new Date();
        lastLoginElement.textContent = formatDate(lastLoginDate);
    }

    function formatDate(date) {
        const options = {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        
        return date.toLocaleDateString('fr-FR', options);
    }

    // Animation d'entrée
    document.querySelector('.container').style.opacity = '0';
    document.querySelector('.container').style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        document.querySelector('.container').style.transition = 'all 0.5s ease';
        document.querySelector('.container').style.opacity = '1';
        document.querySelector('.container').style.transform = 'translateY(0)';
    }, 100);
});