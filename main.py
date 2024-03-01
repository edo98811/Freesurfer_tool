import create_table as t
import prepare as p
import docker as d
import helper_functions as h


class FreesurferTool():
    def __init__(self, save_folder="", destination_folder=""):
        self.SET = h.read_settings_from_json("setting.json")
        self.Docker = d.DockerInstance(self.SET, save_folder, destination_folder)
        self.Table = t.Table(self.SET)
        self.Prepare = p.Prepare(self.SET)

    def load_settings():
        pass


def create_table():
    fs = FreesurferTool()
    fs.Table.create_mris_table()

def run_recon_all():
    fs = FreesurferTool(save_folder="nifti", destination_folder="reconall")
    fs.Prepare.prepare_for_reconall()
    fs.Docker.run("reconall", 120, 10)

def run_samseg():
    fs = FreesurferTool(save_folder="nifti", destination_folder="reconall")
    fs.Prepare.prepare_for_samseg()
    fs.Docker.run("reconall", 120, 10) # to move these two numbers in the settings


if __name__ == "__main__":
    pass

    # get parameters 
    # run function 
# create sh file e fare in modo che si installi correttamente
# scrivere anche comandi per updarte the settings
# add in the settif