-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS mydatabase;

-- Use the database
USE mydatabase;

-- Create the MyURLs table
CREATE TABLE IF NOT EXISTS MyURLs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    urls VARCHAR(255)
);

-- Insert some example data
INSERT INTO MyURLs (urls) VALUES ('www.google.com');
INSERT INTO MyURLs (urls) VALUES ('www.github.com');
INSERT INTO MyURLs (urls) VALUES ('www.stackoverflow.com');
