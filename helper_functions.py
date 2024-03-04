import json
from collections import defaultdict
import os
import sys

def read_settings_from_json(file_path):
    """
    Read settings from a JSON file and return them as a dictionary.
    
    Parameters:
        file_path (str): The path to the JSON file.
    
    Returns:
        dict: A dictionary containing the settings.
    """
    with open(file_path, "r") as json_file:
        settings = json.load(json_file)
    return defaultdict(lambda: [], settings)

def save_settings_to_json(settings, file_path):
    """
    Save settings to a JSON file.
    
    Parameters:
        settings (dict): A dictionary containing the settings.
        file_path (str): The path to save the JSON file.
    """
    with open(file_path, "w") as json_file:
        json.dump(settings, json_file, indent=4)

def create_tmp_folder():
    """
    Create a folder named 'tmp' in the current working directory if it doesn't already exist.
    """
    tmp_folder = os.path.join(os.getcwd(), 'tmp')
    if not os.path.exists(tmp_folder):
        os.mkdir(tmp_folder)


def delete_tmp_folder():
    """
    Delete the folder named 'tmp' in the current working directory if it exists.
    """
    tmp_folder = os.path.join(os.getcwd(), 'tmp')
    if os.path.exists(tmp_folder):
        os.rmdir(tmp_folder)


