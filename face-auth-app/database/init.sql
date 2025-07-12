-- Script d'initialisation de la base de données Face Auth
CREATE DATABASE IF NOT EXISTS face_auth_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE face_auth_db;

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    face_encoding LONGBLOB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME NULL,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_is_active (is_active)
);

-- Données de test (optionnel)
-- INSERT INTO users (username, email, password_hash, is_active) 
-- VALUES ('admin', 'admin@example.com', '$2b$12$test_hash', TRUE);