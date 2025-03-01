'''
pattern of the original file name is numbers_string.extension1
convert it to numbers.extension2
'''

import os
import re

# Change directory if needed
directory = "./data/"

for filename in os.listdir(directory):
    match = re.match(r"^(\d+)_.*\..+$", filename)
    if match:
        new_filename = f"{match.group(1)}.csv"
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_filename}")
