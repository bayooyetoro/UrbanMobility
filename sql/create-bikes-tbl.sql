CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;

CREATE TABLE IF NOT EXISTS silver.bike_trips (
    rental_id TEXT,
    duration INTEGER,
    bike_id TEXT,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    start_station_id TEXT,
    start_station_name TEXT,
    end_station_id TEXT,
    end_station_name TEXT,
    source_file TEXT,
    ingestion_timestamp TIMESTAMP,
    load_date DATE
);