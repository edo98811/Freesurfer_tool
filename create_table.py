import os
import pandas as pd
import string 
import secrets
import json 
import helper_functions as h

class Table():
  def __init__(self, SET):
    self.SET = SET
    self.table = self.create_mris_table()

  def create_mris_table(self):
      self.table = self.create_table_df(os.path.join(self.SET["base_path"], self.SET["dicom_path"]))
      
      self.create_subj_info()
      self.add_processing_info(os.path.join(self.SET["base_path"], self.SET["reconall_path"]), os.path.join(self.SET["base_path"], self.SET["samseg_path"]), os.path.join(self.SET["base_path"], self.SET["nifti_path"]))

      
  def update_mris_table(self, df_path: str):

    self.table = pd.read_excel(df_path)

    self.create_subj_info()
    self.add_processing_info(os.path.join(self.SET["base_path"], self.SET["reconall_path"]), os.path.join(self.SET["base_path"], self.SET["samseg_path"]), os.path.join(self.SET["base_path"], self.SET["nifti_path"]))


# to delete the return value
  def create_table_df(self, base_directory: str):
      
      data = {
        "acquisition": [],
        "mris": [],
        "paths": []
      }

      for root, dirs, _ in os.walk(base_directory):
          # For each subdirectory in the directory
          for MRIdir in dirs:
                
            # Go into the condition only if i reached a directory that containes only files
            if all(os.path.isfile(os.path.join(root, MRIdir, item)) for item in os.listdir(os.path.join(root,MRIdir))): 
            
              # Select the acquisition ID
              acquisition = root.split("/")[-3]
              MRIdir_id = root.split("/")[-2]
              rel_path = os.path.relpath(os.path.join(root, MRIdir), base_directory)

              # If its not the first iteration
              if len(data["acquisition"])!= 0:

                # If it is the same subject (acquisition ID al fondo della lista = acquisition ID attuale)
                if not (data["acquisition"][-1] == acquisition):
                  data["acquisition"].append(acquisition)
                  data["mris"].append([MRIdir_id]) # list because i neet to be able to append to it other mris
                  data["paths"].append([rel_path]) # to convert, it is not in the diret childern
                  
                # it is always the last one in the queue to add
                else:
                  data["mris"][-1].append(MRIdir_id) # in this bloc
                  data["paths"][-1].append(rel_path)
                  
              else: 
                data["acquisition"].append(acquisition)
                data["mris"].append([MRIdir_id]) 
                data["paths"].append([rel_path])
                              
      return pd.DataFrame.from_dict(data)

  def create_subj_info(self):

    self.table["converted"] = [list() for _ in range(len(self.table.index))]
    
    self.table["t1"] = [list() for _ in range(len(self.table.index))]
    
    for rowname, row in self.table.iterrows():
      for mri in row["mris"]:
        if not any(MRI_name_substring in mri for MRI_name_substring in self.SET["file_identifiers"]["T1"]) and not any(MRI_name_substring in mri for MRI_name_substring in self.SET["file_identifiers"]["T1_no"]):
            self.table.at[rowname, "t1"].append(mri)

    self.table["t2"] = [list() for _ in range(len(self.table.index))]
    
    for rowname, row in self.table.iterrows():
      for mri in row["mris"]:
        if not any(MRI_name_substring in mri for MRI_name_substring in self.SET["file_identifiers"]["T2"]) and not any(MRI_name_substring in mri for MRI_name_substring in self.SET["file_identifiers"]["T2_no"]):
            self.table.at[rowname, "t2"].append(mri)

    self.table["flair"] = [list() for _ in range(len(self.table.index))]
    
    for rowname, row in self.table.iterrows():
      for mri in row["mris"]:
        if not any(MRI_name_substring in mri for MRI_name_substring in self.SET["file_identifiers"]["FLAIR"]) and not any(MRI_name_substring in mri for MRI_name_substring in self.SET["file_identifiers"]["FLAIR_no"]):
          self.table.at[rowname, "flair"].append(mri)
    
    self.table["samseg"] = ["Not possible" for x in range(len(self.table.index))]
    
    for rowname, row in self.table.iterrows():

      if len(row["t1"]) >=1 and len(row["t2"]) >=1: 
        self.table.at[rowname, "samseg"] = "Possible - only t2 not fl"
      if len(row["t1"]) >=1 and len(row["flair"]) >=1: 
        self.table.at[rowname, "samseg"] = "Possible"

    self.table["reconall"] = ["Not possible" for x in range(len(self.table.index))]
    
    for rowname, row in self.table.iterrows():

      if len(row["t1"]) >=1: 
        self.table.at[rowname, "reconall"] = "Possible - only t2 not fl"
      if len(row["t1"]) >=1: 
        self.table.at[rowname, "reconall"] = "Possible" 

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
      for i, mri in enumerate(row["mris"]):
        if os.path.isfile(os.path.join(search_path_data, f"{row['acquisition']}", f"{mri}.nii")):
          self.table.at[index, "converted"].append(True)
        else:
          print(f"{os.path.join(search_path_data, f"{row['acquisition']}", f"{mri}.nii")} does not exist")
          self.table.at[index, "converted"].append(False)

  def save_to_excel(self, sheet_name="subjects"):

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
