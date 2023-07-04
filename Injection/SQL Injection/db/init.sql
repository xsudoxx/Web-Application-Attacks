CREATE DATABASE IF NOT EXISTS mydatabase;

USE mydatabase;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255)
);

INSERT INTO users (username, email, password, role)
VALUES ('Admin', 'Admin@hackme.com', 'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3', 'admin');

CREATE TABLE IF NOT EXISTS submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    message TEXT
);
INSERT INTO submissions (name,email,message)
VALUES ('Admin','Admin@hackme.com','There is a known issue with this websites login page, you can by pass the login!!!!')