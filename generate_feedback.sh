#!/bin/bash

# Check if the user provided a directory path
if [ $# -eq 0 ]; then
    echo "Usage: $0 <directory_path>"
    exit 1
fi

# Store the directory path provided by the user
directory_path="$1"

# Iterate through each directory in the provided directory
for group_dir in "$directory_path"*/; do
    feedback_dir="${group_dir}feedback"

    # Check if the feedback directory exists
    if [ ! -d "$feedback_dir" ]; then
        echo "Feedback directory not found for $group_dir"
        continue
    fi

    # Check if feedback_*.md exists, if not, rename feedback_*.pdf.todo to feedback_*.md
    feedback_md=$(find "$feedback_dir" -name "feedback_*.md")
    if [ -z "$feedback_md" ]; then
        feedback_pdf_todo=$(find "$feedback_dir" -name "feedback_*.pdf.todo")
        if [ -n "$feedback_pdf_todo" ]; then
            feedback_basename=$(basename "$feedback_pdf_todo" .pdf.todo)
            rm "$feedback_pdf_todo"
            cp "$directory_path/../$feedback_basename.md" "$feedback_dir"
            feedback_md="$feedback_dir/$feedback_basename.md"
        fi
    fi

    # Iterate through each feedback file in the feedback directory and
    # delete all files except for feedback_*.md
    for feedback_file in "$feedback_dir"/*; do
        if [ "$feedback_file" != "$feedback_md" ]; then
            rm "$feedback_file"
        fi
    done

    # Convert feedback_*.md to feedback_*.pdf
    feedback_pdf=$(basename "$feedback_md" .md).pdf
    pandoc "$feedback_md" -o "$feedback_dir/$feedback_pdf"
done

echo "Conversion complete."

