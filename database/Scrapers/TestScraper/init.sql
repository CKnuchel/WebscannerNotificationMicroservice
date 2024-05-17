CREATE DATABASE IF NOT EXISTS test_scraper_db;

GRANT ALL PRIVILEGES ON auth_db.* TO 'testscraperuser'@'%' IDENTIFIED BY 'testscraperpassword';

FLUSH PRIVILEGES;
