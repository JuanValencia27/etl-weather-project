-- DATABASE CREATION

CREATE DATABASE IF NOT EXISTS weather_etl
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE weather_etl;

-- CITY TABLE

CREATE TABLE IF NOT EXISTS cities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CLIMATE DATA TABLE

CREATE TABLE IF NOT EXISTS weather_data (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    city_id INT NOT NULL,
    date DATE NOT NULL,
    hour TINYINT NOT NULL,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    precipitation DECIMAL(5,2),
    wind_speed DECIMAL(5,2),
    weather_code INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_city
        FOREIGN KEY (city_id)
        REFERENCES cities(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_city_datetime
        UNIQUE (city_id, date, hour)
);







