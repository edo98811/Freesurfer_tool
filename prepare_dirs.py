import os
import shutil
import helper_functions as h

# function to edit to define how the dicom names are created, input are the destination root, the root and the dir of the dicom folder
def _define_directories(root, dir, destination_dir):

    source_subdir = os.path.join(root, dir)
    destination_subdir = os.path.join(destination_dir, f"{root.split('/')[-1]}_{root.split('/')[-1]}")
            
    return source_subdir, destination_subdir


def _move_subdirectories_to_first_level(source_dir, destination_dir):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)
    
    # Iterate through subdirectories in the source directory
    for root, dirs, _ in os.walk(source_dir):
        for directory in dirs:
            
            # if it contains only files
            if all(os.path.isfile(os.path.join(directory, item)) for item in os.listdir(directory)):
 
                source_subdir = os.path.join(root, directory)
                destination_subdir = os.path.join(destination_dir, f"{root.split('/')[-1]}_{root.split('/')[-1]}")
                
                # Move the subdirectory to the destination directory
                shutil.move(source_subdir, destination_subdir)
                print(f"Moved '{source_subdir}' to '{destination_subdir}'")

def _move_subdirectories_to_first_level_old(source_dir, destination_dir):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)
    
    # Iterate through subdirectories in the source directory
    for root, dirs, _ in os.walk(source_dir):
        for directory in dirs:
            
            # if it contains only files
            if all(os.path.isfile(os.path.join(directory, item)) for item in os.listdir(directory)):

                # take the -1 element and set it as name, 
                dicom_first_level = root.split('/')[-1]
                source_subdir = os.path.join(root, directory)
                destination_subdir = os.path.join(destination_dir, dicom_first_level)
                
                # Move the subdirectory to the destination directory
                shutil.move(source_subdir, destination_subdir)
                print(f"Moved '{source_subdir}' to '{destination_subdir}'")

# Example usage:
def process_folders():
    source_directory = h.read_settings_from_json()["dicom_raw"]
    destination_directory = h.read_settings_from_json()["dicom"]
    _move_subdirectories_to_first_level(source_directory, destination_directory)