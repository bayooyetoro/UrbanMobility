CREATE SCHEMA silver;
CREATE SCHEMA gold;

CREATE TABLE IF NOT EXISTS silver.bike_trips (
    rental_id TEXT,
    bike_id TEXT,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    duration INTEGER,
    start_station_id TEXT,
    start_station_name TEXT,
    end_station_id TEXT,
    end_station_name TEXT,
    _ingestion_timestamp TIMESTAMP,
    _load_date DATE,
    _file_name TEXT
);