# Week 1 Homework Commands

## Question 1: Check pip version
```bash
docker run -it --entrypoint bash python:3.13
pip --version
```

## Question 2: Docker networking
Answer based on docker-compose.yaml analysis.

## Data Loading
```bash
# Download data
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet

# Start containers
docker-compose up -d

# Load data
uv run python load_green_nov_2025.py

# Connect to database
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

## Question 3: Count short trips
```sql
SELECT COUNT(*)
FROM green_taxi_nov_2025
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1;
```

## Question 4: Longest trip day
```sql
SELECT 
    DATE(lpep_pickup_datetime) AS pickup_day,
    MAX(trip_distance) AS max_distance
FROM green_taxi_nov_2025
WHERE trip_distance < 100
GROUP BY DATE(lpep_pickup_datetime)
ORDER BY max_distance DESC
LIMIT 1;
```

## Question 5: Biggest pickup zone (Nov 18)
```sql
SELECT 
    z."Zone",
    SUM(g.total_amount) AS total
FROM green_taxi_nov_2025 g
JOIN zones z ON g."PULocationID" = z."LocationID"
WHERE DATE(g.lpep_pickup_datetime) = '2025-11-18'
GROUP BY z."Zone"
ORDER BY total DESC
LIMIT 1;
```

## Question 6: Largest tip from East Harlem North
```sql
SELECT 
    zdo."Zone",
    MAX(g.tip_amount) AS max_tip
FROM green_taxi_nov_2025 g
JOIN zones zpu ON g."PULocationID" = zpu."LocationID"
JOIN zones zdo ON g."DOLocationID" = zdo."LocationID"
WHERE zpu."Zone" = 'East Harlem North'
  AND DATE(g.lpep_pickup_datetime) >= '2025-11-01'
  AND DATE(g.lpep_pickup_datetime) < '2025-12-01'
GROUP BY zdo."Zone"
ORDER BY max_tip DESC
LIMIT 1;
```

## Question 7: Terraform workflow
```bash
terraform init
terraform apply -auto-approve
terraform destroy
```
