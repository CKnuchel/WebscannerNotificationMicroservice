CREATE DATABASE IF NOT EXISTS test_scraper_db;

CREATE USER IF NOT EXISTS 'testscraperuser'@'%' IDENTIFIED BY 'testscraperpassword';

GRANT ALL PRIVILEGES ON test_scraper_db.* TO 'testscraperuser'@'%';

FLUSH PRIVILEGES;
