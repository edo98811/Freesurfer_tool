import json
import sys


def update_json(json_file, field, new_value):
    # Load the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Update the specified field with the new value
    if field in data:
        data[field] = new_value
    else:
        print(f"Field '{field}' not found in JSON file.")
        return

    # Save the updated JSON back to the file
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Field '{field}' updated successfully.")

if __name__ == "__main__":
    # print(len(sys.argv))
    if len(sys.argv) != 4:
        print("Usage: update_settings.py <field_to_update> <new_value>")
        sys.exit(1)

    json_file = "settings.json"
    field_to_update = sys.argv[1]
    new_value = sys.argv[2]

    update_json(json_file, field_to_update, new_value)