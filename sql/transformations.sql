USE weather_etl;

ALTER TABLE weather_data
ADD COLUMN year INT,
ADD COLUMN month INT,
ADD COLUMN month_name VARCHAR(15);


UPDATE weather_data
SET 
    year = YEAR(date),
    month = MONTH(date),
    month_name = MONTHNAME(date);


ALTER TABLE weather_data
ADD COLUMN season VARCHAR(10);


UPDATE weather_data
SET season =
    CASE
        WHEN month IN (12, 1, 2) THEN 'Winter'
        WHEN month IN (3, 4, 5) THEN 'Spring'
        WHEN month IN (6, 7, 8) THEN 'Summer'
        WHEN month IN (9, 10, 11) THEN 'Autumn'
    END;


CREATE OR REPLACE VIEW vw_weather_analysis AS
SELECT
    c.city_name,
    w.date,
    w.hour,
    w.year,
    w.month,
    w.month_name,
    w.season,
    w.temperature,
    w.humidity,
    w.precipitation,
    w.wind_speed
FROM weather_data w
JOIN cities c ON w.city_id = c.id;


SELECT * 
FROM vw_weather_analysis
LIMIT 20;
