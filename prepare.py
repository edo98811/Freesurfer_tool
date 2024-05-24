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

  def prepare_for_conversion(self, cols=["t1", "t2", "t2_flair", "t1_flair"], last=True, move=False)-> None:
    
    source_docker_origin_path = []
    source_docker_destination_path = []

    f = open(f"{self.SET['nifti']}/log.txt", "w")
    for _, row in self.df.iterrows():

      f.write(f"In subject {row['acquisition']}\n")

      # Iterate through the column of which the mris need to be converted
      for col in cols:
        try:
          column = row[col]
        except:
          raise Warning("invalid column {col}")

        rel_paths = row['paths']
        converted = row['converted']
        mris = row['mris']
        
        # If the column contains at least one mri
        if len(column) > 0:

            # in case only one per colum (the last) needs to be converted
            if last:
              column = [column[-1]] # to keep it as a list
              f.write(f"  from column {col} kept image {column}\n")

            # get the indexes of the wanted mris and find the correct rel path
            indexes = [i for i, elem in enumerate(mris) if elem in column]
            rel_paths_to_convert = []
            converted_to_convert = []
            for index in indexes: 

              rel_paths_to_convert.append(rel_paths[index])
              converted_to_convert.append(converted[index])
            
            # iterate though the list of mri to convert
            for last_element, last_path, c in zip(column, rel_paths_to_convert, converted_to_convert):
              # Create the key in the format "subj_id_acquisition"

              if (not c):
                if move:
                  if os.path.exists(os.path.join(self.SET["rawdata"], last_path)):
                    os.makedirs(os.path.join(self.SET["nifti"], row['acquisition']), exist_ok=True)
                    shutil.copy(os.path.join(self.SET["rawdata"], last_path), 
                                    os.path.join(self.SET["nifti"], row['acquisition'], f"{last_element}.nii"))
                  else: 
                    raise Exception("trying to prepare nifti but dicom found, maybe you wanted to use 'convertdicom'")
                else:
                  if not os.path.isfile(os.path.join(self.SET["rawdata"], last_path)):
                    source_docker_origin_path.append(f"/ext/fs-subjects/{last_path}")
                    source_docker_destination_path.append(f"/ext/processed-subjects/{row['acquisition']}/{last_element}.nii")
                  else:
                    raise Exception("trying to convert dicom but file found, maybe you wanted to use 'preparnifti'")
      f.write("\n")
    f.close()

    _save_files(source_docker_origin_path, source_docker_destination_path) 

  def prepare_for_reconall_from_source(self, cols=["t1"], last=True)-> None: # for reconall only t1
    
    source_docker_origin_path = []
    source_docker_destination_path = []

    for _, row in self.df.iterrows():

        # Iterate through the column of which the mris need to be converted
        for col in cols:
          # select column if it exists, otherwise throw warning
          try:
            column = row[col]
          except:
            raise Warning("invalid column {col}")

          rel_paths = row['paths']
          converted = row['converted']
          mris = row['mris']
          
          # If the column contains at least one mri
          if len(column) > 0:

              # in case only one per colum (the last) needs to be converted
              if last:
                column = [column[-1]] # to keep it as a list
                print(f"kept column {column}")

              # get the indexes only of the wanted mris (they are in the searched column)
              indexes = [i for i, elem in enumerate(mris) if elem in column]
              rel_paths_to_convert = []
              converted_to_convert = []

              # Keep only the necessary paths
              for index in indexes: 

                rel_paths_to_convert.append(rel_paths[index])
                converted_to_convert.append(converted[index])
              
              # iterate though the list of mri to convert
              for last_element, last_path, c in zip(column, rel_paths_to_convert, converted_to_convert):
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

        if f"/ext/fs-subjects/{row['acquisition']}/{row["t1"][-1]}.nii" != f"/ext/fs-subjects/{row['acquisition']}/{row["t1"][-1]}.nii".replace(" ", ""):
          print (f"non valid name for freesurfer: /ext/fs-subjects/{row['acquisition']}/{row["t1"][-1]}.nii")
          continue
        
        source_docker_origin_path.append(f"/ext/fs-subjects/{row['acquisition']}/{row["t1"][-1]}.nii")
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
        t2 = eval(row["t2_flair"])[-1] if len(eval(row["t2_flair"])) > 0 else eval(row["t2"])[-1]

        source_docker_origin_path.append(f"/ext/fs-subjects/{row['acquisition']}/{t1}.nii")
        source_docker_origin_path.append(f"/ext/fs-subjects/{row['acquisition']}/{t2}.nii")
        source_docker_destination_path.append(f"{row['acquisition']}")
    
    _save_files(source_docker_origin_path, source_docker_destination_path) 

  def prepare_for_tables(self)-> None:

    subjects = []

    for _, row in self.df.iterrows():
        
        if row["reconall"] == "Done": 

            subject = f"{row['acquisition']}"
            subjects.append(subject)

    with open("tmp/subjects.txt", "w") as fp:
      for item in subjects:
        fp.write(f"{item}\n")
