import os
import pandas as pd
import string 
import secrets
import json 
import helper_functions as h
import ast
import re


# Funtion to modify each time, it returns the aquisition name
def acquisition_name(folder_path, image_name):

  # if it is not nifti or it is a CT scan
  if "CCT " in image_name or not image_name.endswith(".nii"):
    return None
  
  # match this string (r string literal) with the last folder in the root
  pattern = r'^.*?(?=_{2,})'
  result = re.sub(pattern, '', folder_path.split('/')[-1])

  return result
    # For each subdirectory in the directory (returns the acquistion name)
  if folder_path.split('/')[-2].startswith("01"):
    return None
  else:
    return f"{folder_path.split('/')[-2]}_{folder_path.split('/')[-1]}"



def remove_spaces_in_folders(base_directory):
    # Iterate over all items in the base directory
    for item in os.listdir(base_directory):
        item_path = os.path.join(base_directory, item)
        
        # Check if the item is a directory
        if os.path.isdir(item_path):
            # Replace spaces with underscores in the directory name
            new_name = item.replace(" ", "")
            new_path = os.path.join(base_directory, new_name)
            
            # Rename the directory if its name contains spaces
            if new_name != item:
              try: 
                os.rename(item_path, new_path)  
              except: 
                print(f"{item_path} is double")
            
            # Recursively call the function for subdirectories
            remove_spaces_in_folders(new_path)
            
def safe_eval(s: str) -> str:
    try:
        return ast.literal_eval(s)
    except (SyntaxError, ValueError):
        return s


 
class Table():
  def __init__(self, SET): 
    self.SET = SET
    if not os.path.isfile(os.path.join(self.SET["table_path"], self.SET["table_name"])):
      print(f"Creating Table in location: {os.path.join(self.SET["table_path"], self.SET["table_name"])}")
      self.create_mris_table() # posso rendere questo processo migliore? (ad es, la load se esiste, la crea se esiste), magari salvarla e un processo diverso
    else:
      print(f"Updating table in location: {os.path.join(self.SET["table_path"], self.SET["table_name"])}")
      # self.table = pd.read_excel(os.path.join(self.SET["table_path"], self.SET["table_name"]))
      self.update_mris_table()

  def create_mris_table(self):
      self.table = (self.create_table_df(os.path.join(self.SET["dicom"])))

      self.create_subj_info()
      self.add_processing_info(os.path.join(self.SET["reconall"]), os.path.join(self.SET["samseg"]), os.path.join(self.SET["nifti"]))

      
  def update_mris_table(self):

    self.table = pd.read_excel(os.path.join(self.SET["table_path"], self.SET["table_name"]))

    columns_to_apply = ['mris', 'paths', 'converted']
    self.table[columns_to_apply] = self.table[columns_to_apply].map(safe_eval)
    
    self.create_subj_info()
    self.add_processing_info(os.path.join(self.SET["reconall"]), os.path.join(self.SET["samseg"]), os.path.join(self.SET["nifti"]))


# to delete the return value
  def create_table_df(self, base_directory: str, find_type="dicom"):
      remove_spaces_in_folders(base_directory)

      data = {
        "acquisition": [],
        "mris": [],
        "paths": []
      }
      if find_type == "dicom":
        # Iterate through all the directories in base_directory
        for root, dirs, _ in os.walk(base_directory):
            
            # Iterate through all images (or believed to be)
            for dicom_dir in dirs:
                  
              # Go into the condition only if i reached a directory that containes only files (dicom folder)
              if all(os.path.isfile(os.path.join(root, dicom_dir, item)) for item in os.listdir(os.path.join(root,dicom_dir))): 
              
                # Select the acquisition ID ( to change when new type of dataset) 

                # acquisition = f"{root.split('/')[-2]}_{root.split('/')[-1]}"
                acquisition = acquisition_name(root, dicom_dir)
                if acquisition == None:
                  continue
                # acquisition = root.split("/")[-2]

                # Create the relative path between base directory and the dicom dir
                rel_path = os.path.relpath(os.path.join(root, dicom_dir), base_directory)

                # If its not the first iteration
                if len(data["acquisition"])!= 0:

                  # If it is not the same subject (acquisition ID al fondo della lista != acquisition ID attuale)
                  if not (data["acquisition"][-1] == acquisition):
                    data["acquisition"].append(acquisition)
                    data["mris"].append([dicom_dir]) # [] list because i need to be able to append to it other mris
                    data["paths"].append([rel_path]) # to convert, it is not in the direct childern
                    
                  # If it only a new acquisition, but not new subject, the index is the last subject
                  else:
                    data["mris"][-1].append(dicom_dir) 
                    data["paths"][-1].append(rel_path)

                # If it is the first iteration, this is needed because of this data["acquisition"][-1]  if condition 
                else: 
                  data["acquisition"].append(acquisition)
                  data["mris"].append([dicom_dir]) 
                  data["paths"].append([rel_path])

      elif find_type == "nifti":

        # Iterate through all the directories in base_directory
        for root, dirs, niis in os.walk(base_directory):
            
            # Iterate through all images (or believed to be)
            for nii_file in niis:
                  
              # Go into the condition only if i reached a nii file
              if nii_file.endswith(".nii"):
              
                # Select the acquisition ID ( to change when new type of dataset) 

                # acquisition = f"{root.split('/')[-2]}_{root.split('/')[-1]}"
                acquisition = acquisition_name(root, nii_file)
                if acquisition == None:
                  continue
                # acquisition = root.split("/")[-2]

                # Create the relative path between base directory and the dicom dir
                rel_path = os.path.relpath(os.path.join(root, nii_file), base_directory)

                # nii file to be saved without extension in order for all the rest to work (it works without eextension)
                nii_file = nii_file[:-4]

                # If its not the first iteration
                if len(data["acquisition"])!= 0:

                  # If it is not the same subject (acquisition ID al fondo della lista != acquisition ID attuale)
                  if not (data["acquisition"][-1] == acquisition):
                    data["acquisition"].append(acquisition)
                    data["mris"].append([nii_file]) # [] list because i need to be able to append to it other mris
                    data["paths"].append([rel_path]) # to convert, it is not in the direct childern
                    
                  # If it only a new acquisition, but not new subject, the index is the last subject
                  else:
                    data["mris"][-1].append(nii_file) 
                    data["paths"][-1].append(rel_path)

                # If it is the first iteration, this is needed because of this data["acquisition"][-1]  if condition 
                else: 
                  data["acquisition"].append(acquisition)
                  data["mris"].append([nii_file]) 
                  data["paths"].append([rel_path])
      
      else: 
        raise ValueError("find_type has invalid value (dicom or nifti)")
      
      return pd.DataFrame.from_dict(data)

  def create_subj_info(self):

    self.table["converted"] = [list() for _ in range(len(self.table.index))]
    
    self.table["t1"] = [list() for _ in range(len(self.table.index))]
    
    for rowname, row in self.table.iterrows():
      for mri in row["mris"]:
        if any(MRI_name_substring in mri for MRI_name_substring in self.SET["file_identifiers"]["T1"]) and not any(MRI_name_substring in mri for MRI_name_substring in self.SET["file_identifiers"]["T1_no"]):
            self.table.at[rowname, "t1"].append(mri)

    self.table["t2"] = [list() for _ in range(len(self.table.index))]
    
    for rowname, row in self.table.iterrows():
      for mri in row["mris"]:
        if any(MRI_name_substring in mri for MRI_name_substring in self.SET["file_identifiers"]["T2"]) and not any(MRI_name_substring in mri for MRI_name_substring in self.SET["file_identifiers"]["T2_no"]):
            self.table.at[rowname, "t2"].append(mri)

    self.table["flair"] = [list() for _ in range(len(self.table.index))]
    
    for rowname, row in self.table.iterrows():
      for mri in row["mris"]:
        if any(MRI_name_substring in mri for MRI_name_substring in self.SET["file_identifiers"]["FLAIR"]) and not any(MRI_name_substring in mri for MRI_name_substring in self.SET["file_identifiers"]["FLAIR_no"]):
          self.table.at[rowname, "flair"].append(mri)
    
    self.table["samseg"] = ["Not possible" for x in range(len(self.table.index))]
    
    for rowname, row in self.table.iterrows():

      if len(row["t1"]) >=1 and len(row["t2"]) >=1: 
        self.table.at[rowname, "samseg"] = "Possible - only t2 not fl"
      elif len(row["t1"]) >=1 and len(row["flair"]) >=1: 
        self.table.at[rowname, "samseg"] = "Possible"

    self.table["reconall"] = ["Not possible" for x in range(len(self.table.index))]
    
    for rowname, row in self.table.iterrows():

      if len(row["t1"]) >=1: 
        self.table.at[rowname, "reconall"] = "Possible"
      if len(row["t1"]) >=1: 
        self.table.at[rowname, "reconall"] = "Possible" 

    # Delete rows that dont contain any useful MRIs (can delete if not needed)
    for rowname, row in self.table.iterrows():
      if len(row["t1"]) == 1 and len(row["flair"]) == 0 and len(row["t2"]):
        self.table = self.table.drop(rowname, axis=0)

  def add_processing_info(self, search_path_reconall: str, search_path_samseg: str, search_path_data: str) -> None:


    # Checks if samseg was run
    for index, row in self.table.iterrows():
      destination_folder = os.path.join(search_path_reconall, f"{row['acquisition']}")
      # print(destination_folder)
      if os.path.exists(destination_folder):
        
        if os.listdir(f"{destination_folder}/stats"):
          self.table.at[index, "reconall"] = "Done"
        else: 
          self.table.at[index, "reconall"] = "Error (or in progress)"
    
    # Check if reconall was run
    for index, row in self.table.iterrows():
      destination_folder = os.path.join(search_path_data, f"{row['acquisition']}", "flair_t2_reg.nii")
      # print(os.path.exists(destination_folder))
      if os.path.exists(destination_folder):
        self.table.at[index, "samseg"] = "Prepared"
      destination_folder = os.path.join(search_path_samseg, f"{row['acquisition']}")
      if os.path.exists(destination_folder):
        self.table.at[index, "samseg"] = "Done"

    # Check if nifti is present
    for index, row in self.table.iterrows():
      for _ , mri in enumerate(row["mris"]):
        if ".nii" in mri:
          continue
        if os.path.isfile(os.path.join(search_path_data, f"{row['acquisition']}", f"{mri}.nii")):
          self.table.at[index, "converted"].append(True)
        else:
          # nifti_folder = os.path.join(search_path_data, f"{row['acquisition']}", f"{mri}.nii")
          # print(f"NIFTI: {nifti_folder} does not exist")
          self.table.at[index, "converted"].append(False)

  def save_table(self, sheet_name="subjects"):

      excel_filename = os.path.join(self.SET["table_path"], self.SET["table_name"])
      # Create a Pandas Excel writer using the XlsxWriter engine
      writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')

      # Write the self.table to the Excel file
      self.table.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1, header=False)

      # Get the xlsxwriter workbook and worksheet objects
      workbook  = writer.book
      worksheet = writer.sheets[sheet_name]

      # Add a header format with bold and a border
      header_format = workbook.add_format({'bold': True, 'border': 1, 'align': 'center', 'valign': 'vcenter'})

      # Write the column headers with the defined format
      for col_num, value in enumerate(self.table.columns.values):
          worksheet.write(0, col_num, value, header_format)
      
      num_rows, num_cols = self.table.shape
      worksheet.add_table(0, 0, num_rows + 1, num_cols - 1, {'columns': [{'header': column} for column in self.table.columns], 'style': None})
      # worksheet.add_table(0, 0, num_rows, num_cols - 1)

      # Close the Pandas Excel writer and save the Excel file
      writer._save()
