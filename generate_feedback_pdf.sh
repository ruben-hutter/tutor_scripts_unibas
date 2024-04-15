#!/bin/bash

# Check if the user provided a directory path
if [ $# -eq 0 ]; then
    echo "Usage: $0 <directory_path>"
    exit 1
fi

# Store the directory path provided by the user
directory_path="$1"

# Iterate through each directory in the provided directory
for dir in "$directory_path"/*/; do
    # Check if the directory contains a feedback directory
    if [ -d "${dir}feedback" ]; then
        # Iterate through each Markdown file in the feedback directory
        for md_file in "${dir}feedback"/*.md; do
            # Extract the filename without extension
            filename=$(basename "$md_file" .md)
            # Remove all files except for the Markdown file
            find "${dir}feedback" -type f ! -name "$(basename "$md_file")" -delete
            echo "Removed unnecessary files in ${dir}feedback"
            # Convert Markdown file to PDF using pandoc
            pandoc "$md_file" -o "${dir}feedback/${filename}.pdf"
            echo "Converted $md_file to ${dir}feedback/${filename}.pdf"
        done
    fi
done

echo "Conversion complete."

