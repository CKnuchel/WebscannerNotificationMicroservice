-- Auth DB
CREATE DATABASE IF NOT EXISTS auth_db;

-- Create and grant privileges to the auth user
CREATE USER IF NOT EXISTS 'auth_api'@'%' IDENTIFIED WITH 'caching_sha2_password' BY 'place_a_guid';
GRANT ALL PRIVILEGES ON auth_db.* TO 'auth_api'@'%';
FLUSH PRIVILEGES;

USE auth_db;
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(100) NOT NULL,
    role VARCHAR(50) DEFAULT 'user'
);

-- other DB's