# Data Dictionary

## Diagram Legend

| Color | Meaning |
|---|---|
| 🟩 Green | Field added or derived in that layer (audit fields, renamed fields, calculated metrics, SCD Type 2 columns). |
| 🟧 Orange | Field whose values are enforced from the station dimension (`stations_cleansed`) instead of being taken from the original trip record. |
| ⬜ No color | Field carried over from the previous layer without changes. |

## Naming Conventions

| Element | Value |
|---|---|
| Catalog | `bikes` |
| Schemas | `landing`, `bronze`, `silver`, `gold` |
| Landing volume | `/Volumes/bikes/landing/data_sources` |
| {system} | Name of the bike-share system (e.g. `divvy`, `baywheels`). |
| {city} | Name of the city in snake_case (e.g. `chicago`, `san_francisco`). |
| `{year}`, `{month}`, `{year-month}` | Period of the data being ingested. |

## Landing

**Catalog:** `bikes` · **Schema:** `landing` · **Volume:** `/Volumes/bikes/landing/data_sources`

### Trip data file

**Path:** `../{system}/trips/{year-month}/{year}{month}_{system}_tripdata.csv`

| Field | Description |
|---|---|
| ride_id | Unique identifier of the trip. |
| rideable_type | Type of vehicle used (`classic_bike`, `electric_bike`). |
| started_at | Date and time the trip started, in the city's local time. |
| ended_at | Date and time the trip ended, in the city's local time. |
| start_station_name | Name of the station where the trip started. |
| start_station_id | Identifier of the station where the trip started. |
| end_station_name | Name of the station where the trip ended. |
| end_station_id | Identifier of the station where the trip ended. |
| start_lat | Latitude where the trip started. |
| start_lng | Longitude where the trip started. |
| end_lat | Latitude where the trip ended. |
| end_lng | Longitude where the trip ended. |
| member_casual | Rider type: `member` (subscriber) or `casual` (single ride or day pass). |

### Station lookup file

**Path:** `../{system}/stations/{year-month}/{system}_stations_lookup.json`

| Field | Description |
|---|---|
| station_id | Unique identifier of the station. |
| name | Public name of the station. |
| short_name | Short name or alternative identifier of the station. |
| address | Street address of the station. |
| lon | Longitude of the station. |
| lat | Latitude of the station. |
| region_id | Identifier of the region the station belongs to. |
| capacity | Total number of docking points at the station. |
| rental_uris.android | Deep link to rent a bike at this station from the Android app. |
| rental_uris.ios | Deep link to rent a bike at this station from the iOS app. |

## Bronze

**Catalog:** `bikes` · **Schema:** `bronze`

### {city}_trips_raw

| Field | Description |
|---|---|
| city | City the trip belongs to, in snake_case. |
| ride_id | Unique identifier of the trip. |
| rideable_type | Type of vehicle used (`classic_bike`, `electric_bike`). |
| started_at | Date and time the trip started, in the city's local time. |
| ended_at | Date and time the trip ended, in the city's local time. |
| start_station_name | Name of the station where the trip started. |
| start_station_id | Identifier of the station where the trip started. |
| end_station_name | Name of the station where the trip ended. |
| end_station_id | Identifier of the station where the trip ended. |
| start_lat | Latitude where the trip started. |
| start_lng | Longitude where the trip started. |
| end_lat | Latitude where the trip ended. |
| end_lng | Longitude where the trip ended. |
| member_casual | Rider type: `member` or `casual`. |
| processed_timestamp | Date and time the record was loaded into this table. |

### {city}_station_lookup_raw

| Field | Description |
|---|---|
| city | City the station belongs to, in snake_case. |
| station_id | Unique identifier of the station. |
| name | Public name of the station. |
| short_name | Short name or alternative identifier of the station. |
| address | Street address of the station. |
| lon | Longitude of the station. |
| lat | Latitude of the station. |
| region_id | Identifier of the region the station belongs to. |
| capacity | Total number of docking points at the station. |
| rental_uris.android | Deep link to rent a bike at this station from the Android app. |
| rental_uris.ios | Deep link to rent a bike at this station from the iOS app. |
| processed_timestamp | Date and time the record was loaded into this table. |

## Silver

**Catalog:** `bikes` · **Schema:** `silver`

### trips_cleansed

> **Rule:** trips with a null start or end station are discarded.

| Field | Description |
|---|---|
| city | City the trip belongs to, in snake_case. |
| ride_id | Unique identifier of the trip. |
| rideable_type | Type of vehicle used (`classic_bike`, `electric_bike`). |
| started_at | Date and time the trip started, in the city's local time. |
| ended_at | Date and time the trip ended, in the city's local time. |
| start_station_name | Name of the station where the trip started. |
| start_station_id | Identifier of the station where the trip started. |
| end_station_name | Name of the station where the trip ended. |
| end_station_id | Identifier of the station where the trip ended. |
| start_lat | Latitude where the trip started. |
| start_lng | Longitude where the trip started. |
| end_lat | Latitude where the trip ended. |
| end_lng | Longitude where the trip ended. |
| member_casual | Rider type: `member` or `casual`. |
| processed_timestamp | Date and time the record was loaded into this table. |

### stations_cleansed

> **SCD Type 2 rules:**
> - A new version of a station is created when any of these fields changes: `name`, `short_name`, `longitude`, `latitude`, `region_id`.
> - The current version of a station is the one with `valid_to` = `NULL`.

| Field | Description |
|---|---|
| city | City the station belongs to, in snake_case. |
| station_id | Unique identifier of the station. |
| name | Public name of the station. |
| short_name | Short name or alternative identifier of the station. |
| address | Street address of the station. |
| longitude | Longitude of the station (renamed from `lon`). |
| latitude | Latitude of the station (renamed from `lat`). |
| region_id | Identifier of the region the station belongs to. |
| capacity | Total number of docking points at the station. |
| valid_from | Date and time from which this version of the station is valid. |
| valid_to | Date and time until which this version of the station was valid. `NULL` for the current version. |

### trips_enriched

> **Rules:**
> - Start and end stations are matched against `stations_cleansed` by `station_id`.
> - Trips whose start or end station is not found in `stations_cleansed` are discarded.

| Field | Description |
|---|---|
| city | City the trip belongs to, in snake_case. |
| ride_id | Unique identifier of the trip. |
| rideable_type | Type of vehicle used (`classic_bike`, `electric_bike`). |
| started_at | Date and time the trip started, in the city's local time. |
| ended_at | Date and time the trip ended, in the city's local time. |
| trip_duration_mins | Duration of the trip in whole minutes, between `started_at` and `ended_at`. |
| start_station_name | Name of the start station, taken from `stations_cleansed`. |
| end_station_name | Name of the end station, taken from `stations_cleansed`. |
| start_latitude | Latitude of the start station, taken from `stations_cleansed`. |
| start_longitude | Longitude of the start station, taken from `stations_cleansed`. |
| end_latitude | Latitude of the end station, taken from `stations_cleansed`. |
| end_longitude | Longitude of the end station, taken from `stations_cleansed`. |
| stations_distance | Straight-line distance in **miles** between the start and end stations, calculated with the Haversine formula. |
| member_casual | Rider type: `member` or `casual`. |
| processed_timestamp | Date and time the record was loaded into this table. |

## Gold

**Catalog:** `bikes` · **Schema:** `gold`

### daily_trip_summary

| Field | Description |
|---|---|
| city | City the metrics belong to, in snake_case. |
| date | Date of the trips, based on `started_at` in the city's local time. |
| total_trips | Total number of trips. |
| total_classic_bike_trips | Number of trips made with a classic bike. |
| total_electric_bike_trips | Number of trips made with an electric bike. |
| avg_trip_duration | Average trip duration, in minutes. |
| max_trip_duration | Longest trip duration, in minutes. |
| min_trip_duration | Shortest trip duration, in minutes. |
| avg_stations_distance | Average distance between start and end stations, in miles. |
| max_stations_distance | Longest distance between start and end stations, in miles. |
| min_stations_distance | Shortest distance between start and end stations, in miles. |
