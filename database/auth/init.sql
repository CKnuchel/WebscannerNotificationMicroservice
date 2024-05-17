-- Initialize the database
CREATE DATABASE IF NOT EXISTS auth_db;

-- Grant permissions to the authuser from any host
GRANT ALL PRIVILEGES ON auth_db.* TO 'authuser'@'%' IDENTIFIED BY 'authpassword';

-- Apply the changes
FLUSH PRIVILEGES;
