-- Initialize the database
CREATE DATABASE IF NOT EXISTS test_scraper_db;

-- Grant permissions to the testscraperuser from any host
GRANT ALL PRIVILEGES ON auth_db.* TO 'testscraperuser'@'%' IDENTIFIED BY 'testscraperpassword';

-- Apply the changes
FLUSH PRIVILEGES;
