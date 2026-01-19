USE weather_etl;

SELECT 
    c.city_name,
    COUNT(*) AS total_records
FROM weather_data w
JOIN cities c ON w.city_id = c.id
GROUP BY c.city_name
ORDER BY total_records DESC;



SELECT 
    MIN(date) AS min_date,
    MAX(date) AS max_date
FROM weather_data;


SELECT 
    c.city_name,
    MIN(w.date) AS min_date,
    MAX(w.date) AS max_date
FROM weather_data w
JOIN cities c ON w.city_id = c.id
GROUP BY c.city_name;



SELECT 
    city_id,
    date,
    hour,
    COUNT(*) AS duplicates
FROM weather_data
GROUP BY city_id, date, hour
HAVING COUNT(*) > 1;



SELECT 
    COUNT(*) AS null_temperature
FROM weather_data
WHERE temperature IS NULL;
SELECT COUNT(*) FROM weather_data WHERE humidity IS NULL;
SELECT COUNT(*) FROM weather_data WHERE precipitation IS NULL;
SELECT COUNT(*) FROM weather_data WHERE wind_speed IS NULL;
