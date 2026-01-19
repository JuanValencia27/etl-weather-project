# ETL WEATHER PROJECT


# DB CONNECTION + CITY LOADING

import requests
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG, CITIES
from datetime import datetime
from config import START_DATE, END_DATE


# FUNCTION: CONNECTION TO MYSQL

def get_db_connection():
    """
    Crea y devuelve una conexión a la base de datos MySQL
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error conectando a MySQL: {e}")
        return None
    

# FUNCTION: GET CITIES FROM MYSQL

def get_cities_from_db():
    """
    Devuelve todas las ciudades almacenadas en la tabla cities
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT id, city_name, latitude, longitude FROM cities"
    cursor.execute(query)

    cities = cursor.fetchall()

    cursor.close()
    connection.close()

    return cities


# FUNCTION: OBTAIN HISTORICAL CLIMATE DATA

def get_weather_data(latitude, longitude):
    """
    Consulta la API de Open-Meteo para datos climáticos horarios
    """
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
            "weather_code"
        ],
        "timezone": "UTC"
    }

    response = requests.get(url, params=params, timeout=30)

    if response.status_code != 200:
        print("Error consultando clima")
        return None

    return response.json()


# FUNCTION: INSERT CLIMATE DATA

def insert_weather_data():
    """
    Inserta datos climáticos horarios en la tabla weather_data
    """
    cities = get_cities_from_db()

    connection = get_db_connection()
    cursor = connection.cursor()

    insert_query = """
        INSERT IGNORE INTO weather_data (
            city_id,
            date,
            hour,
            temperature,
            humidity,
            precipitation,
            wind_speed,
            weather_code
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    for city in cities:
        city_id = city["id"]
        city_name = city["city_name"]
        print(f"DEBUG -> city_id: {city_id}, city_name: {city_name}")


        print(f"Extrayendo clima para {city_name}")

        data = get_weather_data(
            city["latitude"],
            city["longitude"]
        )

        if data is None or "hourly" not in data:
            print(f"Sin datos para {city_name}")
            continue

        times = data["hourly"]["time"]
        temperatures = data["hourly"]["temperature_2m"]
        humidity = data["hourly"]["relative_humidity_2m"]
        precipitation = data["hourly"]["precipitation"]
        wind_speed = data["hourly"]["wind_speed_10m"]
        weather_code = data["hourly"]["weather_code"]

        rows = []

        for i in range(len(times)):
            dt = datetime.fromisoformat(times[i])
            rows.append((
                city_id,
                dt.date(),
                dt.hour,
                temperatures[i],
                humidity[i],
                precipitation[i],
                wind_speed[i],
                weather_code[i]
            ))

        try:
            cursor.executemany(insert_query, rows)
            connection.commit()
            print(f"{len(rows)} registros insertados para {city_name}")
        except Error as e:
            print(f"Error insertando datos para {city_name}: {e}")
            connection.rollback()

    cursor.close()
    connection.close()



# FUNCTION: OBTAIN COORDINATES (GEOCODING API)

def get_city_coordinates(city_name, country):
    """
    Consulta la API de Open-Meteo Geocoding
    y devuelve latitud y longitud
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        print(f"Error API para {city_name}")
        return None, None

    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        print(f"No se encontraron coordenadas para {city_name}")
        return None, None

    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]

    return latitude, longitude


# FUNCTION: INSERT CITIES INTO MYSQL

def insert_cities():
    """
    Inserta las ciudades con sus coordenadas
    en la tabla cities
    """
    connection = get_db_connection()
    if connection is None:
        return

    cursor = connection.cursor()

    insert_query = """
        INSERT INTO cities (city_name, country, latitude, longitude)
        VALUES (%s, %s, %s, %s)
    """

    for city in CITIES:
        city_name = city["city_name"]
        country = city["country"]

        print(f"Procesando ciudad: {city_name}")

        latitude, longitude = get_city_coordinates(city_name, country)

        if latitude is None or longitude is None:
            print(f"Saltando {city_name}")
            continue

        try:
            cursor.execute(
                insert_query,
                (city_name, country, latitude, longitude)
            )
            connection.commit()
            print(f"{city_name} insertada correctamente")

        except Error as e:
            print(f"Error insertando {city_name}: {e}")
            connection.rollback()

    cursor.close()
    connection.close()


# MAIN

if __name__ == "__main__":
    # insert_cities()  
    insert_weather_data()

