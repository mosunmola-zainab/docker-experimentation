# Data Engineering Pipeline - NYC Taxi Data

A containerized data ingestion pipeline built with Docker, PostgreSQL, and Python for processing large-scale NYC taxi trip data.

## Project Overview

This project demonstrates end-to-end data engineering skills including:
- Docker containerization
- PostgreSQL database management
- Python data pipelines with pandas
- SQL analytics and data quality checks
- Infrastructure as code with Docker Compose

## Tech Stack

- **Python 3.13** - Data processing
- **PostgreSQL 18** - Database
- **Docker & Docker Compose** - Containerization
- **pandas** - Data manipulation
- **SQLAlchemy** - Database connectivity
- **pgAdmin** - Database management UI
- **uv** - Python package manager

## Dataset

- **Source**: NYC Taxi & Limousine Commission (TLC)
- **Records**: 1.3+ million taxi trips
- **Period**: January 2021
- **Size**: ~180MB compressed

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- 2GB+ free disk space

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd pipeline
```

2. Start the infrastructure:
```bash
docker-compose up -d
```

3. Access pgAdmin at `http://localhost:8085`:
   - Email: `admin@admin.com`
   - Password: `root`

### Load Data

**Load taxi trip data:**
```bash
docker run -it \
  --network=pipeline_default \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table=yellow_taxi_trips \
    --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```

**Load zones lookup table:**
```bash
uv run python load_zones.py
```

## Project Structure
```
pipeline/
├── docker-compose.yaml    # Multi-container orchestration
├── Dockerfile            # Ingestion script container
├── ingest_data.py        # Main data pipeline script
├── load_zones.py         # Zone lookup data loader
├── notebook.ipynb        # Exploratory data analysis
├── pyproject.toml        # Python dependencies
└── README.md            # This file
```

## Key Features

### Chunked Data Processing
Handles large files efficiently by processing in 100k row chunks to avoid memory issues.

### Dockerized Pipeline
Complete reproducibility - runs anywhere Docker is installed.

### Data Quality Checks
SQL queries to identify NULL values and invalid location IDs.

### pgAdmin Integration
Web-based database management for easy data exploration.

## 📈 SQL Analytics Examples

**Count trips by day:**
```sql
SELECT 
    CAST(tpep_dropoff_datetime AS DATE) AS day,
    COUNT(1) AS trip_count
FROM yellow_taxi_trips
GROUP BY day
ORDER BY day;
```

**Join with location names:**
```sql
SELECT 
    t.*,
    CONCAT(z."Borough", ' | ', z."Zone") AS pickup_location
FROM yellow_taxi_trips t
JOIN zones z ON t."PULocationID" = z."LocationID"
LIMIT 100;
```

## Cleanup

**Stop containers (keep data):**
```bash
docker-compose down
```

**Remove all Docker resources:**
```bash
docker-compose down
docker system prune -a --volumes
```

## Learning Outcomes

- Containerization best practices
- Large-scale data ingestion
- Database schema design
- SQL analytics and JOINs
- Infrastructure as Code (IaC)
- Data quality assessment

## Author

**Zainab Hassan**
- Focus: Data Engineering & MLOps

## Acknowledgments

Built as part of the [DataTalks.Club Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)

## License

This project is open source and available under the MIT License.
