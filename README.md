# Bike Trips Data Pipeline with Databricks

Which trips cover the longest distances? Which areas of the city are most popular among cyclists? At what time of day are bikes used the most? This project is a Databricks pipeline that provides different users with high-quality data on daily bike trips.

## Objective

Provide BI developers, data analysts and data scientists with clean, reliable data on bike trips, extracted and processed from the public bike-share systems of different cities.

## Solution

The pipeline extracts data from [Bay Wheels](https://lyftbikes.com/system-data) (San Francisco) and [Divvy](https://divvybikes.com/system-data) (Chicago), both operated by Lyft. Each system publishes open data on all the trips taken every month, along with real-time information about its bike stations.

### Architectural and Technical Decisions

- **Batch pipeline:** since each system publishes its data monthly, there is no need for streaming or event-driven processing. A job scheduled to run once a month is enough.
- **Medallion Architecture:** splitting the pipeline into layers improves maintainability, makes debugging easier, improves data quality step by step, and supports governance and scalability.
- **SCD Type 2:** bike station locations can change over time, so keeping the history of every station keeps the trip data accurate.
- **PySpark:** the monthly data volume does not exceed 1 GB, so a single-node library such as Pandas or Polars would be enough for this workload. PySpark was chosen to apply and demonstrate distributed processing skills, and it leaves the pipeline ready to scale as more cities are added.
- **Databricks:** provides an environment that fits naturally with the Medallion Architecture and comes with Apache Spark built in.
- **Delta Lake:** offers time travel, data versioning and efficient upserts. It also enforces schemas, which can be relaxed to accept new columns added to the data sources.

### Architecture

#### High-Level Architecture

1. **Landing and Bronze layers**
   - The landing layer downloads the monthly bike trips CSV and the bike stations snapshot JSON, and stores them in a volume.
   - The bronze layer reads those files and appends them to the raw Delta tables, adding only audit fields.
2. **Silver layer**
   - Merges the bike trips from all cities, discards trips without a start or end station, and appends them to the cleansed trips Delta table.
   - Merges the bike station snapshots from all cities and applies the SCD Type 2 process to track new and updated stations.
   - Joins trips and stations, calculates trip metrics, and appends the result to the enriched trips Delta table.
3. **Gold layer**
   - Aggregates the enriched trips by city and day, and appends them to the daily trip summary Delta table, ready for monthly reporting.

![High-Level Diagram](img/high_level_diagram.png)

#### Data Architecture

See the full [Data Dictionary](./data_dictionary.md).

![Data Architecture](img/data_architecture.png)

#### Low-Level Architecture

1. **ingest_bike_trips:** downloads the CSV with the bike trips of a specific month and city.
2. **ingest_stations_lookup:** downloads the JSON with the current snapshot of a city's bike stations.
3. **bike_trips_raw:** reads the month's CSV from the volume, adds the `city` and `processed_timestamp` audit columns, and appends it to the city's raw Delta table.
4. **stations_lookup_raw:** reads the month's JSON from the volume, adds the `city` and `processed_timestamp` audit columns, and appends it to the city's raw Delta table.
5. **bike_trips_cleansed:** reads the raw bike trips tables of all cities, merges them, and appends them to the cleansed trips Delta table.
6. **stations_lookup:** reads the raw station tables of all cities, merges them, renames `lon`/`lat` to `longitude`/`latitude`, and applies the SCD Type 2 process (`valid_from`/`valid_to`) to new and updated stations.
7. **bike_trips_enriched:** joins the month's bike trips with the stations, calculates `trip_duration_mins` and `stations_distance` (Haversine distance), and appends the result to the enriched trips Delta table.
8. **bike_trips_summary:** aggregates the month's enriched trips by `city` and `date`, calculates the daily metrics, and appends them to the daily trip summary Delta table.

> **Note:** pipeline tasks run with parameters defined in the [pipeline configuration](transformations/bikes_pipeline.yaml).

![Low-Level Diagram](img/low_level_diagram.png)

## Requirements

- Databricks Runtime: 18 LTS
- Apache Spark: 4.1.0
- Languages: Python, SQL

## Installation and Setup

<!-- TODO -->

## Project Structure

<!-- TODO -->

## Future Improvements

- Reflect San Francisco's rebranding from **Bay Wheels** to **Lyft Bike**.
- Add other US public bike-share systems, such as [Citi Bike](https://citibikenyc.com/system-data) (New York–New Jersey), [Capital Bikeshare](https://capitalbikeshare.com/system-data) (Washington, D.C.) and [Bluebikes](https://bluebikes.com/system-data) (Boston).
- Join bike trips data with pricing plans.

## Contact Me

If you're passionate about technology, or if you're looking for a dedicated Systems Engineer, let's connect! Feel free to send me a message.

Santiago Burbano Puin | [LinkedIn](https://www.linkedin.com/in/santiago-burbano-puin/) | [santibur444@gmail.com](mailto:santibur444@gmail.com)
