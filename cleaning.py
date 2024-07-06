import json
import os

import json


def format_data(input_file_path, output_file_path):
    """
    Reads the input JSON file, formats the data, and writes it to the output file.
    """
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        modified_data = []

        for line in input_file:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                print(f"Error decoding JSON in line: {line}")
                continue

            # Extracting the relevant part from the title
            title = entry.get('title', '').strip()
            title_parts = title.split('،')
            relevant_part = title_parts[1].strip() if len(title_parts) >= 2 else title.strip()

            # Remove " م² |" from the area field
            area = entry.get('area', '').replace(" م² |", "")

            # Extract description field
            description = entry.get('description', '').strip()

            # Constructing the dictionary with the desired format
            formatted_entry = {
                "title": relevant_part,
                "price": entry.get('price', ''),
                "beds": entry.get('beds', ''),
                "living_rooms": entry.get('living_rooms', ''),
                "bathrooms": entry.get('bathrooms', ''),
                "area": area,
                "description": description  # Include description in the formatted data
            }

            modified_data.append(formatted_entry)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(modified_data, output_file, ensure_ascii=False, indent=4)


def count_valid_entries(data):
    """
    Counts the number of entries that have no empty values and whose title contains 'حي'.
    """
    return sum(
        1 for entry in data
        if all(entry.values()) and "حي" in entry['title']
    )

import json
import os

def filter_data(input_file_path, output_file_path):
    """
    Loads data from the JSON file, filters out dictionaries with any empty values and titles not containing 'حي',
    and writes the filtered data back to a JSON file.
    """
    # Load data from the JSON file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Remove any newline characters from the description field
    for entry in data:
        if 'description' in entry:
            entry['description'] = entry['description'].replace('\n', '')

    # Filter out dictionaries with any empty values and titles not containing 'حي'
    filtered_data = [
        entry for entry in data
        if all(entry.values()) and "حي" in entry['title']
    ]

    # Write the filtered data back to a JSON file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)

    print(f"Filtered data has been saved to '{output_file_path}'.")




def main():
    # Paths for input and output files
    input_file_path = 'North-riyadh-apartments.json'
    formatted_output_file_path = 'TestFORMAT.json'
    filtered_output_file_path = 'filtered_data.json'

    # Format the data and write to output file
    format_data(input_file_path, formatted_output_file_path)

    # Load the formatted data from the output file
    with open(formatted_output_file_path, 'r', encoding='utf-8') as file:
        formatted_data = json.load(file)

    # Count the number of valid entries
    valid_entries_count = count_valid_entries(formatted_data)

    # Print the count
    print(f"Number of entries with no empty values and titles containing 'حي': {valid_entries_count}")

    # Filter the formatted data and save to a new file
    filter_data(formatted_output_file_path, filtered_output_file_path)
    os.remove(input_file_path)
    os.remove(formatted_output_file_path)

if __name__ == "__main__":
    main()
