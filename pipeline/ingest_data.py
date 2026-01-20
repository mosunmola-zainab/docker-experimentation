import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click

# Data type specifications
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]

@click.command()
@click.option('--user', default='root', help='PostgreSQL user')
@click.option('--password', default='root', help='PostgreSQL password')
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--port', default=5432, type=int, help='PostgreSQL port')
@click.option('--db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--table', default='yellow_taxi_data', help='Target table name')
@click.option('--url', required=True, help='URL of the CSV file to ingest')
def ingest_data(user, password, host, port, db, table, url):
    """Ingest CSV data into PostgreSQL database"""
    
    # Create database connection
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    print(f"Connecting to database: {db}")
    print(f"Target table: {table}")
    print(f"Data source: {url}")
    
    # Create iterator for chunked reading
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=100000
    )
    
    # Get first chunk
    first_chunk = next(df_iter)
    
    # Create table
    first_chunk.head(0).to_sql(
        name=table,
        con=engine,
        if_exists="replace"
    )
    print(f"Table '{table}' created")
    
    # Insert first chunk
    first_chunk.to_sql(
        name=table,
        con=engine,
        if_exists="append"
    )
    print(f"Inserted first chunk: {len(first_chunk)} rows")
    
    # Insert remaining chunks
    for df_chunk in tqdm(df_iter, desc="Loading data"):
        df_chunk.to_sql(
            name=table,
            con=engine,
            if_exists="append"
        )
    
    print("Data ingestion complete!")

if __name__ == '__main__':
    ingest_data()