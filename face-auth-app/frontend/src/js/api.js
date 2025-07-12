// Module API pour communiquer avec le backend
class API {
    constructor() {
        this.baseURL = 'http://localhost:8000';
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || 'Erreur de requête');
            }
            
            return data;
        } catch (error) {
            console.error('Erreur API:', error);
            throw error;
        }
    }

    async register(userData) {
        return this.request('/api/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async login(credentials) {
        return this.request('/api/login', {
            method: 'POST',
            body: JSON.stringify(credentials)
        });
    }

    async faceLogin(faceData) {
        return this.request('/api/face-login', {
            method: 'POST',
            body: JSON.stringify(faceData)
        });
    }

    async getUser(userId) {
        return this.request(`/api/users/${userId}`);
    }
}

// Instance globale de l'API
const api = new API();

// Fonctions utilitaires pour les messages
function showMessage(element, message, type = 'info') {
    if (!element) return;
    
    element.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    
    // Supprimer le message après 5 secondes
    setTimeout(() => {
        element.innerHTML = '';
    }, 5000);
}

function setButtonLoading(button, loading = true) {
    if (!button) return;
    
    const textElement = button.querySelector('.btn-text') || button;
    const originalText = button.dataset.originalText || textElement.textContent;
    
    if (!button.dataset.originalText) {
        button.dataset.originalText = originalText;
    }
    
    if (loading) {
        button.disabled = true;
        textElement.innerHTML = '<span class="loading"></span> Chargement...';
    } else {
        button.disabled = false;
        textElement.textContent = originalText;
    }
}

// Gestion du stockage local
const storage = {
    setUser(user) {
        localStorage.setItem('currentUser', JSON.stringify(user));
    },
    
    getUser() {
        const user = localStorage.getItem('currentUser');
        return user ? JSON.parse(user) : null;
    },
    
    removeUser() {
        localStorage.removeItem('currentUser');
    }
};

// Navigation entre les pages
function navigateToPage(page) {
    const { ipcRenderer } = require('electron');
    ipcRenderer.invoke('navigate-to-page', page);
}