import os
import sys

def rename_directories(parent_directory):
    # Iterate over each directory in the parent directory
    for directory_name in os.listdir(parent_directory):
        # Check if the item is a directory
        if os.path.isdir(os.path.join(parent_directory, directory_name)):
            # Split the directory name by "_", and select the part after the first "_"
            new_name = '_'.join(directory_name.split('_')[1:])
            # Construct the full paths for the old and new directory names
            old_path = os.path.join(parent_directory, directory_name)
            new_path = os.path.join(parent_directory, new_name)
            # Rename the directory
            os.rename(old_path, new_path)
            print(f"Renamed {old_path} to {new_path}")

def main(args):
    if len(args) != 2:
        print("Usage: python rename_directories.py <parent_directory>")
        sys.exit(1)

    # Specify the path to the parent directory
    parent_directory = sys.argv[1]

    if not os.path.isdir(parent_directory):
        print(f"Error: {parent_directory} is not a directory")
        sys.exit(1)

    # Call the function to rename directories
    rename_directories(parent_directory)

if __name__ == "__main__":
    main(sys.argv)
