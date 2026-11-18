INSERT INTO gold.dim_station (
    station_id,
    station_name
)
SELECT DISTINCT
    start_station_id,
    start_station_name
FROM silver.bike_trips
WHERE start_station_id IS NOT NULL
UNION
SELECT DISTINCT
    end_station_id,
    end_station_name
FROM silver.bike_trips
WHERE end_station_id IS NOT NULL;