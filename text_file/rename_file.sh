#!/bin/bash

FOLDER="./data"  # Specify the target folder

for file in "$FOLDER"/*.txt; do
    if [[ -f "$file" ]]; then
        filename=$(basename -- "$file")  # Extract filename
        new_name=$(echo "$filename" | sed -E 's/^([0-9]+)_.*\..+$/\1.csv/')
        mv "$file" "$FOLDER/$new_name"
        echo "Renamed: $filename -> $new_name"
    fi
done
