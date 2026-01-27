import pandas as pd
from sqlalchemy import create_engine

# Read parquet
df = pd.read_parquet('green_tripdata_2025-11.parquet')

# Create database connection
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

# Load to database
df.to_sql(name='green_taxi_nov_2025', con=engine, if_exists='replace', index=False)

print(f"Loaded {len(df)} trips into 'green_taxi_nov_2025' table")
print(f"Columns: {list(df.columns)}")
