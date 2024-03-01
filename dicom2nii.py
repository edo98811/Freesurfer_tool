import os
import dicom2nifti
import pandas as pd
import subprocess
import shutil

source_dir = "/mnt/S/edoardoStorage/Pipeline_MRI2/PPMI/"
destination_dir = "/mnt/S/edoardoStorage/Pipeline_MRI2/PPMI_nifti/"


def convert_dicom_to_nifti(dicom_folder, output_folder, output_name):

    # print(f"running conversion on {dicom_folder}")
    # Create output folder if it doesn"t exist
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)
    
    # Use dicom2nifti to convert DICOM to NIfTI
    try:
        command = [
        "docker", "run",
        "-v", f"{dicom_folder}:/input",
        "-v", f"{output_folder}:/output",
        "3565ebb52045",
        "-o", "/output",
        "-f", output_name,
        "/input"
        ]
        if os.path.exists(f"{output_folder}/{output_name}"):
          # If it exists, delete the entire directory and its contents
          shutil.rmtree(f"{output_folder}/{output_name}")
        print(command)
        subprocess.run(command, check=True)
        print("Conversion successful.")
    except Exception as e:
        print("Conversion failed with error:", e)
        
"""     try:
      os.rename(current_file, output_name)
      print("File renamed successfully.")
    except OSError as e:
      print(f"Error: {e}") """

def main(df, last=False, cols=['mris']):

    for _, row in df.iterrows():

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
                # source_docker_origin_path.append(f"/{source_dir}/{last_path}")
                # source_docker_destination_path.append(f"{destination_dir}/{row["acquisition"]}/{last_element}.nii")
                # dicom_folder= f"/{source_dir}/{last_path}"
                # output_folder = f"{destination_dir}/{row['acquisition']}/{last_element}.nii"
                # output_file = f"{last_element}.nii"
                
                dicom_folder = "/" + source_dir + "/" + last_path
                output_folder = destination_dir + "/" + str(row['acquisition']) + "/"
                output_file = f"{last_element}.nii"
                convert_dicom_to_nifti(dicom_folder, output_folder, output_file)


    	           

if __name__=="__main__":
  df = pd.read_excel("MRI_table_with_results.xlsx")
  main(df)