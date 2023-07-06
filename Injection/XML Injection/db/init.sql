CREATE DATABASE IF NOT EXISTS mydatabase;

USE mydatabase;

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    phone_number VARCHAR(20)
);

INSERT INTO employees (name, email, password, phone_number)
VALUES
    ('John Smith', 'john.smith@example.com', 'password123', '1234567890'),
    ('Jane Johnson', 'jane.johnson@example.com', 'passw0rd', '9876543210'),
    ('Michael Davis', 'michael.davis@example.com', 'securepass', '5555555555'),
    ('Emily Wilson', 'emily.wilson@example.com', 'strongpassword', '1111111111'),
    ('Daniel Brown', 'daniel.brown@example.com', '12345678', '9999999999'),
    ('Olivia Taylor', 'olivia.taylor@example.com', 'password', '7777777777'),
    ('David Miller', 'david.miller@example.com', 'password123', '8888888888'),
    ('Sophia Wilson', 'sophia.wilson@example.com', 'qwerty', '6666666666');
