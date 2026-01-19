USE weather_etl;

-- Rainiest cities (ranking)
SELECT
    city_name,
    ROUND(SUM(precipitation), 2) AS total_precipitation_mm
FROM vw_weather_analysis
GROUP BY city_name
ORDER BY total_precipitation_mm DESC;

-- Average temperature by season
SELECT
    season,
    ROUND(AVG(temperature), 2) AS avg_temperature_c
FROM vw_weather_analysis
GROUP BY season
ORDER BY avg_temperature_c DESC;

-- Average temperature by city and season (most powerful)
SELECT
    city_name,
    season,
    ROUND(AVG(temperature), 2) AS avg_temperature_c
FROM vw_weather_analysis
GROUP BY city_name, season
ORDER BY city_name, avg_temperature_c DESC;

-- Comparison between years (2023 vs. 2024)
SELECT
    city_name,
    year,
    ROUND(AVG(temperature), 2) AS avg_temperature_c,
    ROUND(SUM(precipitation), 2) AS total_precipitation_mm
FROM vw_weather_analysis
GROUP BY city_name, year
ORDER BY city_name, year;

-- City with the greatest temperature variability
SELECT
    city_name,
    ROUND(MAX(temperature) - MIN(temperature), 2) AS temp_variability
FROM vw_weather_analysis
GROUP BY city_name
ORDER BY temp_variability DESC;
