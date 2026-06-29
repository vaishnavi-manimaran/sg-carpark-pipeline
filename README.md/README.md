# SG Carpark Availability Pipeline

A real-time data pipeline tracking live parking availability across Singapore, built end-to-end with Python, SQLite, and Power BI.

## Overview

This project ingests live carpark availability data from a public Singapore government API on an automated schedule, joins it against static HDB carpark reference data, and visualizes the result in an interactive Power BI dashboard. It mirrors the architecture of my [SG Transport Data Pipeline](https://github.com/vaishnavi-manimaran/sg-transport-data-pipeline) project — live API + scheduled automation + relational SQLite storage + Power BI — applied to a different domain (parking instead of buses) to demonstrate the same data engineering pattern is repeatable, not a one-off.

## Data Sources

- **Live data:** [data.gov.sg Carpark Availability API](https://api.data.gov.sg/v1/transport/carpark-availability) — real-time lot counts updated roughly every minute, covering HDB, LTA, and URA carparks across Singapore.
- **Static reference data:** [HDB Carpark Information dataset](https://data.gov.sg) — address, coordinates (SVY21), parking type, and operating details for 2,266 HDB carparks.

## Pipeline Architecture

```
Live API (data.gov.sg) ──┐
                          ├──> Python (requests) ──> SQLite (carparks.db) ──> Power BI (ODBC)
Static HDB dataset ───────┘
```

1. **Static data ingestion** (`fetch_carpark_info.py`) — pulls all 2,266 HDB carpark records via the `datastore_search` API, paginated in batches of 1,000.
2. **Coordinate conversion** (`convert_coords.py`) — converts carpark locations from SVY21 (Singapore's local survey grid, EPSG:3414) to standard latitude/longitude using `pyproj`, and assigns each carpark a region (North/South/East/West/Central) based on the converted coordinates.
3. **Database setup** (`setup_database.py`) — creates two SQLite tables: `carparks` (static reference data with location/region) and `carpark_availability` (live readings).
4. **Live ingestion** (`ingest_live_data.py`) — fetches the live API and inserts a timestamped row per carpark per lot type into `carpark_availability`.
5. **Automation** — `ingest_live_data.py` runs every 10 minutes via Windows Task Scheduler, with no manual intervention required.
6. **Visualization** — Power BI connects directly to the live SQLite database via an ODBC driver, so the dashboard reflects current data on refresh rather than a static export.

## Results

As of this writing, the pipeline has been running continuously and unattended for **just under 3 days**, collecting:

- **185,724 total readings** across **77 automated runs**
- Collection spanning **26–29 June 2026**, every ~10 minutes, with zero manual intervention
- **2,266 static carparks** geocoded and assigned to one of five regions

### Regional breakdown (current snapshot)

| Region | Lots Available |
|---|---|
| North | ~1,93,000 |
| East | ~1,24,000 |
| West | ~81,000 |
| Central | ~76,000 |
| South | ~30,000 |

*(Figures reflect a live snapshot and change continuously as the pipeline runs; see dashboard for current values.)*

## Dashboard

The Power BI dashboard includes:
- **KPI card** — total lots available right now, citywide
- **Region breakdown table** — live availability by region, with conditional-formatting color scale
- **Interactive map** — every carpark plotted by location, bubble-sized by current availability, color-coded by region, with address/carpark-ID tooltips
- **Hour-of-day trend** — availability patterns by time of day, using a calculated column extracted from each reading's timestamp
- **Slicers** — filter the entire dashboard by region and by hour of day

## Technical Notes

- The live API includes LTA/URA carparks in addition to HDB ones, so a small fraction of live readings (~1,300 rows) don't have a matching static record — these are correctly excluded from the regional breakdown rather than silently miscounted.
- SVY21-to-WGS84 coordinate conversion uses the official EPSG:3414 definition via `pyproj`, not a hand-rolled formula.
- Timestamps are parsed from text into true DAX datetime values (`DATEVALUE`/`TIMEVALUE`) to support hour-of-day extraction, since the source format wasn't automatically recognized by Power BI's type converter.
- "Current" availability is computed with a DAX measure that finds each carpark's most recent reading independently (`SUMX` over `VALUES(carpark_number)`), rather than summing across all historical readings — a common pitfall when working with append-only time-series data.

## Tech Stack

Python (`requests`, `pyproj`, `sqlite3`) · SQLite · Power BI · DAX · Windows Task Scheduler · ODBC

## Tools Used

- `fetch_carpark_info.py` — static dataset ingestion
- `convert_coords.py` — coordinate conversion & region assignment
- `setup_database.py` — database schema creation
- `ingest_live_data.py` — live data ingestion (scheduled task)
- `sg_carpark_dashboard.pbix` — Power BI dashboard
