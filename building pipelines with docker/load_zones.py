import pandas as pd
from sqlalchemy import create_engine

# Read zones CSV
df = pd.read_csv('taxi_zone_lookup.csv')

# Create database connection
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

# Load to database
df.to_sql(name='zones', con=engine, if_exists='replace', index=False)

print(f"Loaded {len(df)} zones into 'zones' table")
print(df.head())
