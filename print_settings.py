import json

# Load JSON data from file
with open("settings.json", "r") as json_file:
    json_data = json.load(json_file)

# Print each field and its corresponding value
print(f" ")
print(f" ")
for key, value in json_data.items():
    print(f"    {key}: {value}")
    print(f" ")
print(f" ")