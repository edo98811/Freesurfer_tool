from typing import List
import os
import shutil
import pandas as pd
import argparse
import helper_functions as h


# Helper functions 
def _save_files(source_docker_origin_path, source_docker_destination_path) -> None:
  h.create_tmp_folder()

  with open("tmp/origins.txt", "w") as fp:
    for item in source_docker_origin_path:
      fp.write(f"{item}\n")
  with open("tmp/destinations.txt", "w") as fp:
    for item in source_docker_destination_path:
      fp.write(f"{item}\n")

def _remove_spaces(data_path: str) -> None:

    original_directory = os.getcwd() 
    os.chdir(data_path)
    
    for old_directory, _, files in os.walk(data_path):
      new_directory = old_directory.replace(" ", "")  # Remove spaces from the folder name
      
      if old_directory != new_directory:
          os.rename(old_directory, new_directory)
          print(f"{old_directory} renamed to {new_directory}")
          
      os.chdir(original_directory)
      
# Data preparation 
class Prepare():
  def __init__(self, SET, table):
    self.df = table.table
    self.SET = SET

  def prepare_for_conversion(self, cols=["mris"], last=False)-> None:
    
    source_docker_origin_path = []
    source_docker_destination_path = []

    for _, row in self.df.iterrows():

        for col in cols:
          column = eval(row[col])
          rel_paths = eval(row['paths'])
          converted = eval(row['converted'])
          
          if column:

              if last:
                column = column[-1]

              
              for last_element, last_path, c in zip(column, rel_paths, converted):
                # Create the key in the format "subj_id_acquisition"
                if (not c):
                  source_docker_origin_path.append(f"/ext/fs-subjects/{last_path}")
                  source_docker_destination_path.append(f"/ext/processed-subjects/{row['acquisition']}/{last_element}.nii")

    _save_files(source_docker_origin_path, source_docker_destination_path) 

  def prepare_for_reconall(self)-> None:
    
    source_docker_origin_path = []
    source_docker_destination_path = []

    for _, row in self.df.iterrows():

      if row["reconall"] == "Possible":

        source_docker_origin_path.append(f"/ext/fs-subjects/{row['acquisition']}/{eval(row["t1"])[-1]}.nii")
        source_docker_destination_path.append(f"{row['acquisition']}")
    
    _save_files(source_docker_origin_path, source_docker_destination_path) 
        
  def prepare_for_samseg(self)-> None:
    
    source_docker_origin_path = []
    source_docker_destination_path = []

    for _, row in self.df.iterrows():

      if row["samseg"] == "Prepared":
        t1 = eval(row["t1"])[-1]
        
        # Add the paths to the origins and destination file
        source_docker_origin_path.append(f"/ext/fs-subjects/{row['acquisition']}/{t1}.nii")
        source_docker_origin_path.append(f"/ext/fs-subjects/{row['acquisition']}/flair_t2_reg.nii")
        source_docker_destination_path.append(f"{row['acquisition']}") # /ext/processed-subjects/
    
    _save_files(source_docker_origin_path, source_docker_destination_path) 

  def prepare_for_registration(self)-> None:
    
    source_docker_origin_path = []
    source_docker_destination_path = []

    for _, row in self.df.iterrows():

      if row["samseg"] == "Possible" or row["samseg"] == "Possible - only t2 not fl":
        t1 = eval(row["t1"])[-1]
        t2 = eval(row["flair"])[-1] if len(eval(row["flair"])) > 0 else eval(row["t2"])[-1]

        source_docker_origin_path.append(f"/ext/fs-subjects/{row['acquisition']}/{t1}.nii")
        source_docker_origin_path.append(f"/ext/fs-subjects/{row['acquisition']}/{t2}.nii")
        source_docker_destination_path.append(f"{row['acquisition']}")
    
    _save_files(source_docker_origin_path, source_docker_destination_path) 
