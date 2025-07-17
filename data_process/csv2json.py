"""
This script reads a CSV file and converts it to JSON format.
The separator of CSV file is expected to be space.
"""

# the first row will be used as header row, where each value  becomes a key (field name) in the resulting JSON objects.
import pandas as pd

# Read the CSV file
df = pd.read_csv("../data/csv_json.csv",delim_whitespace=True)  # Replace with your actual CSV file path

# Convert DataFrame to JSON
# orient="records": Each row is converted into a dictionary.
# lines=False: Writes all data as a single JSON array.
# indent=4: Makes the JSON output human-readable and indented with 4 spaces.
df.to_json("csv_json.json", orient="records", lines=False, indent=4)


import json

# Custom field names
custom_fields = ["alpha", "beta", "gamma"]

# Read space-separated values from CSV (no header)
rows = []
with open("../data/csv_json.csv", "r") as f:
    for line in f:
        values = line.strip().split()
        if len(values) != len(custom_fields):
            print(f"Skipping line due to field count mismatch: {line.strip()}")
            continue
        row = dict(zip(custom_fields, values))
        rows.append(row)

# Write JSON output
with open("output.json", "w") as f:
    json.dump(rows, f, indent=4)

print("Conversion completed. Output written to output.json.")