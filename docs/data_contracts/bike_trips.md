# Bike Trips Data Contract

## Source

Transport for London (TfL) Santander Cycle Hire Data

## Dataset Description

Journey-level records representing individual bike hires.

## Refresh Frequency

Monthly

## Landing Zone

data/bronze/bikes/

## Primary Business Entity

Bike Trip

## Expected Schema

| Column | Type | Nullable | Description |
|----------|----------|----------|----------|
| Rental Id | Long | No | Unique rental identifier |
| Duration | Integer | No | Journey duration in seconds |
| Bike Id | Integer | No | Bike identifier |
| End Date | Timestamp | No | Journey end timestamp |
| EndStation Id | Integer | Yes | Destination station id |
| EndStation Name | String | Yes | Destination station name |
| Start Date | Timestamp | No | Journey start timestamp |
| StartStation Id | Integer | Yes | Origin station id |
| StartStation Name | String | Yes | Origin station name |

## Quality Rules

### Critical

- Rental Id must be unique
- Duration > 0
- Start Date not null
- End Date not null

### Warning

- StartStation Id may be null
- EndStation Id may be null

## Bronze Rules

Bronze preserves source records exactly as received.

Additional metadata columns:

| Column | Type |
|----------|----------|
| source_file | String |
| ingestion_timestamp | Timestamp |
| load_date | Date |

## Silver Rules

- Remove duplicates on Rental Id
- Reject Duration <= 0
- Reject missing Start Date
- Reject missing End Date

Invalid records written to:

data/quarantine/bikes/

## Target Table

silver.bike_trips