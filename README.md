# 📊 Weather ETL & Climate Analysis Project

## Project Overview
This project implements a **complete ETL pipeline** that extracts historical weather data from a public API, stores it in a relational database (MySQL), transforms the data for analysis, and finally visualizes insights through an interactive **Power BI dashboard**.

The main objective is to demonstrate practical skills in:
- API consumption
- Data modeling and validation
- SQL analytics
- Business-oriented data visualization

---

## ETL Workflow

### 1️⃣ Extract
- Source: **Open-Meteo Historical Weather API**
- Hourly historical weather data
- Time range: **2023–2024**
- Multiple cities across different regions

### 2️⃣ Load
- Database: **MySQL**
- Core tables:
  - `cities`
  - `weather_data`
- Controlled inserts to avoid duplicates

### 3️⃣ Transform
- Temporal derived fields:
  - Year
  - Month
  - Month name
  - Season
- Analytical view:
  - `vw_weather_analysis`

---

## Data Analysis

Business-oriented questions addressed:
- Which cities have the highest accumulated precipitation?
- How does average temperature vary by season?
- Are there significant differences between years (2023 vs 2024)?
- Which cities show higher temperature variability?

All analytical queries are available in:



---

## Power BI Dashboard

The dashboard enables:
- Comparison of total precipitation by city
- Seasonal average temperature analysis
- Filtering by city and year
- High-level climate KPIs visualization

### Key Climate KPIs
- Average temperature (°C)
- Average humidity (%)
- Total precipitation (mm)
- Total weather records

---

## Data Quality & Validation

Data validation checks include:
- No null values in critical fields
- No duplicated weather records
- Valid date range (2023–2024)
- Referential consistency between cities and weather data

Validation queries are available in:

---

## Technologies Used

- Python 3.11
- MySQL
- SQL
- Power BI
- Open-Meteo API

---

## Future Improvements

- Climate analysis by hemisphere
- Temperature anomaly detection
- ETL automation (scheduled execution)
- Power BI Service deployment

---

## Database Configuration

Before running the project, update the database credentials in config.py


## Author

- Juan José Cardeño Valencia
- Data Analytics Portfolio Project
