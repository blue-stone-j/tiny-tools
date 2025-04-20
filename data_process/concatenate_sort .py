import os
import pandas as pd

# Path to the folder with CSV files
folder_path = './folder_path'
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

def read_with_key(file_path):
    df = pd.read_csv(file_path, header=None)
    key = df.iloc[1].tolist()  # Use entire second row as sort key
    return key, df

# Read all CSVs and collect them with their sort keys
csv_blocks = []
for filename in csv_files:
    path = os.path.join(folder_path, filename)
    key, df = read_with_key(path)
    csv_blocks.append((key, df))

# Sort the CSV blocks using the second row
csv_blocks.sort(key=lambda x: x[0])

# Concatenate all dataframes
result_df = pd.concat([df for _, df in csv_blocks], ignore_index=True)

# Save to a new file
result_df.to_csv('merged_sorted_by_second_row.csv', index=False, header=False)

