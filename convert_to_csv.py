import json
import csv

def convert_json_to_csv(input_file_path, output_file_path):
    """
    Converts JSON data to CSV format.
    """
    # Load JSON data
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Specify CSV header and field names
    fieldnames = ["title", "price", "beds", "living_rooms", "bathrooms", "area", "description"]

    # Write to CSV file
    with open(output_file_path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            # Write each entry to CSV, ensuring proper encoding for Arabic characters
            writer.writerow({
                "title": entry["title"],
                "price": entry["price"],
                "beds": entry["beds"],
                "living_rooms": entry["living_rooms"],
                "bathrooms": entry["bathrooms"],
                "area": entry["area"],
                "description": entry["description"]
            })

    print(f"CSV data has been saved to '{output_file_path}'.")

# Example usage:
input_file_path = 'filtered_data.json'  # Replace with your input JSON file path
output_file_path = 'output.csv'  # Replace with your desired output CSV file path

convert_json_to_csv(input_file_path, output_file_path)
