#!/bin/bash

# Check if directory is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

TARGET_DIR="$1"

# Function to check if a file is a text file or a specific extension
is_target_file() {
    file_type=$(file --mime-type "$1" | awk '{print $2}')
    case "$file_type" in
        text/*) return 0 ;;
    esac

    case "$1" in
        *.cpp|*.h|*.hpp|*.cmake|*.txt) return 0 ;;
    esac

    return 1
}

# Process only the target files
find "$TARGET_DIR" -type f | while read -r file; do
    if is_target_file "$file"; then
        dos2unix "$file"
        echo "Converted: $file"
    fi
done

echo "Conversion completed."

