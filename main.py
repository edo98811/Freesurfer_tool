import create_table as t
import prepare as p
import docker as d
import helper_functions as h
import argparse

# TODO: move number of iteration for docker as parameter or in setting

class FreesurferTool():
    def __init__(self, save_folder="", destination_folder=""):
        self.SET = h.read_settings_from_json("settings.json")
        self.Docker = d.DockerInstance(self.SET, save_folder, destination_folder)
        self.Table = t.Table(self.SET)
        self.Prepare = p.Prepare(self.SET)

    def load_settings():
        pass


def create_table():
    fs = FreesurferTool()
    fs.Table.create_mris_table()
    fs.Table.save_to_excel()

def run_recon_all():
    fs = FreesurferTool(save_folder="nifti", destination_folder="reconall")
    fs.Prepare.prepare_for_reconall()
    fs.Docker.run("reconall", 120, 10)

def run_samseg():
    fs = FreesurferTool(save_folder="nifti", destination_folder="reconall")
    fs.Prepare.prepare_for_samseg()
    fs.Docker.run("samseg", 120, 10) 

def registration():
    fs = FreesurferTool(save_folder="nifti", destination_folder="reconall")
    fs.Prepare.prepare_for_samseg()
    fs.Docker.run("registration", 120, 10) 



def run_selected_function(args) -> None:

    if args.option == "table":
        create_table()
    elif args.option == "samseg":
        run_samseg()
    elif args.option == "reconall":
        run_recon_all()
    elif args.option == "registration":
        registration()
    else:
        print("Invalid option. Please provide a valid option.")

def main()-> None :

    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description="To run freesurfer tool")
    
    # Add argument for the function selection
    parser.add_argument("option", type=str, help="Write the name of a function")
    
    # Parse the command-line arguments
    args = parser.parse_args()

    run_selected_function(args)
    
if __name__=="__main__":
  
  main()