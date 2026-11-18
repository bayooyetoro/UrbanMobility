CREATE TABLE IF NOT EXISTS gold.dim_station (
    station_key SERIAL PRIMARY KEY,
    station_id INTEGER,
    station_name TEXT,
    record_created_at TIMESTAMP DEFAULT NOW()
);