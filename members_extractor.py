import csv
import json

# Read data from CSV file
def read_csv(file_path):
    data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            data.append(row)
    return data

# Format data into desired structure
def format_data(csv_data):
    formatted_data = []
    for row in csv_data:
        formatted_row = [[row[2], row[1], row[3]]]  # Reordering name and surname
        formatted_data.append(formatted_row)
    return formatted_data

# Write formatted data to JSON file
def write_json(data, file_path):
    with open(file_path, 'w') as jsonfile:
        json.dump({"Ruben": data}, jsonfile, indent=4)

# Main function
def main():
    csv_file_path = '2024_03_21_18-511711043458_member_export_1935437.csv'  # Change this to the path of your CSV file
    json_file_path = 'members.json'  # Change this to the desired output JSON file path

    # Read data from CSV file
    csv_data = read_csv(csv_file_path)

    # Format data
    formatted_data = format_data(csv_data)

    # Write formatted data to JSON file
    write_json(formatted_data, json_file_path)

if __name__ == "__main__":
    main()

