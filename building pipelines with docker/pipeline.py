import sys
import pandas as pd
print("arguments", sys.argv)

day = int(sys.argv[1])
print(f"Running pipeline for day {day}")

# Example operation: create a simple DataFrame
df = pd.DataFrame({"day": [1, 2, 3], "num_passengers": [4, 5, 6]})
print(df.head())

# save to parquet file
df.to_parquet(f"output_day_{sys.argv[1]}.parquet")