update_settings() {
    # Check if the JSON file exists
    file="settings.json"
    if [ ! -f "$file" ]; then
        echo "Error: JSON file '$file' not found."
        return 1
    fi

    # Check if jq is installed
    if ! command -v jq &> /dev/null; then
        echo "Error: jq is not installed. Please install jq to use this function."
        return 1
    fi

    # Ask the user for the key and new content
    read -p "Enter the key to update: " key
    read -p "Enter the new content: " new_content

    # Update the JSON file
    jq --arg key "$key" --arg new_content "$new_content" '.[$key] = $new_content' "$file" > tmp.json && mv tmp.json "$file"
    echo "JSON file '$file' updated successfully."
}

fstool(){
    python3 "main.py" "$@"
}