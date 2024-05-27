import create_table as t
import prepare as p
import docker as d
import helper_functions as h
import argparse
import prepare_dirs as pd


N1 = 120
N2 = 20

class FreesurferTool():
    def __init__(self, origin_folder="rawdata", destination_folder="nifti", start_type="dicom"):
        self.SET = h.read_settings_from_json("settings.json")
        self.Docker = d.DockerInstance(self.SET, origin_folder, destination_folder)
        self.Table = t.Table(self.SET, find_type=start_type)
        self.Prepare = p.Prepare(self.SET, self.Table)

    # to implement?
    def load_settings():
        pass


def create_table(start_type="dicom"):
    fs = FreesurferTool(start_type=start_type)
    fs.Table.save_table()

def convert_dicom():
    fs = FreesurferTool(origin_folder="rawdata", destination_folder="nifti")
    fs.Prepare.prepare_for_conversion()
    # fs.Docker.debugging_container("convertdicom")
    fs.Docker.run("convertdicom", N1, N2)

def prepare_nifti():
    fs = FreesurferTool(origin_folder="rawdata", destination_folder="nifti")
    fs.Prepare.prepare_for_conversion(move=True)

def run_recon_all():
    fs = FreesurferTool(origin_folder="nifti", destination_folder="reconall")
    fs.Prepare.prepare_for_reconall()
    fs.Docker.run("reconall", N1, N2)

def run_samseg():
    fs = FreesurferTool(origin_folder="nifti", destination_folder="samseg")
    fs.Prepare.prepare_for_samseg()
    fs.Docker.run("samseg", N1, N2) 

def registration():
    fs = FreesurferTool(origin_folder="nifti", destination_folder="nifti")
    fs.Prepare.prepare_for_registration()
    fs.Docker.run("register", N1, N2) 

# def prepare_dicom():
#    pd.process_folders()

def fs_tables():
    fs = FreesurferTool(origin_folder="reconall", destination_folder="reconall")
    fs.Prepare.prepare_for_tables()
    fs.Docker.run("create_tables", 1, 1) 

def run_selected_function(args) -> None:

    if args.option == "table":
        create_table()
    if args.option == "tablenifti":
        create_table(start_type="nifti")
    elif args.option == "samseg":
        run_samseg()
    elif args.option == "convertdicom":
        convert_dicom()
    elif args.option == "preparenifti":
        prepare_nifti()
    elif args.option == "reconall":
        run_recon_all()
    elif args.option == "register":
        registration()
    elif args.option == "fstables":
        fs_tables()
    # elif args.option == "dicom_prepare":
    #     prepare_dicom()
    else:
        print("Invalid option. Please provide a valid option.")

def main() -> None :

    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description="To run freesurfer tool")
    
    # Add argument for the function selection
    parser.add_argument("option", type=str, help="Write the name of a function")
    parser.add_argument("--N1", type=int, default=120, help="total number of images to process")
    parser.add_argument("--N2", type=int, default=20, help="number of images per container")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    global N1 
    N1 = args.N1
    global N2 
    N2 = args.N2

    run_selected_function(args)
    
if __name__=="__main__":
  
  main()