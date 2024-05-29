import subprocess
from datetime import datetime 
import helper_functions as h
import math
import os

class DockerInstance():
    def __init__(self, SET, source, destination):
        self.source = source
        self.destination = destination
        self.SET = SET
    
    def _command_function(self, max_number: int) -> list[str]:
        return [ # " ".join(
                "docker", "run", "--rm", "--name", f"edoardo_freesurfer_{max_number}",
                "-v", f"{self.SET["license_path"]}:/license.txt:ro",
                "-v", f"{self.SET["app_path"]}/freesurfer_all.sh:/root/freesurfer.sh",
                "-v", f"{self.SET["app_path"]}/tmp:/info:ro",
                "-v", f"{self.SET[self.destination]}:/ext/processed-subjects",
                "-v", f"{self.SET[self.source]}:/ext/fs-subjects",
                "-e", "FS_LICENSE=license.txt",
                "1b0f81a8cb9f",
                "sh", "freesurfer.sh"
            ]
        
    def run(self, function, n_subj, per_loop, log_file="log.txt"):

        n_loops = math.ceil(n_subj/per_loop)
        
        # TODO: add check on source and destination
        # TODO: put the command creation in a function because it is the same for both
        logf = os.path.join(self.SET["base_path"], "docker_logs")
        if not os.path.exists(logf):
            os.makedirs(logf)

        start = 0
        print(f"Total containers to be run: {n_loops}, for {n_subj} total subjects and max {per_loop} per container")
        print("")

        # Set container index
        try:
            container_list = subprocess.check_output("docker container ls --format '{{.Names}}' | grep '^edoardo_freesurfer_'", shell=True).decode().splitlines()
            max_number = 0
            for container in container_list:
                number = int(container.split("_")[-1])
                if number > max_number:
                    max_number = number
        except:
            max_number = 0

        with open(log_file, "a") as log:
            log.write(f"on {datetime.now()} containers started: \n")

        for i in range(n_loops):
            end = start + per_loop
            max_number += 1
            # print(f"Iteration: {i+1}")
            print(f"running container edoardo_freesurfer_{max_number}")
            # print(f"with parameters sh freesurfer.sh {function} {start} {end}")

            with open(log_file, "a") as log:
                log.write(f"    edoardo_freesurfer_{max_number}\n")

            command = [ # " ".join(
                "docker", "run", "--rm", "--name", f"edoardo_freesurfer_{max_number}",
                "-v", f"{self.SET["license_path"]}:/license.txt:ro",
                "-v", f"{self.SET["app_path"]}/freesurfer_all.sh:/root/freesurfer.sh",
                "-v", f"{self.SET["app_path"]}/tmp:/info:ro",
                "-v", f"{self.SET[self.destination]}:/ext/processed-subjects",
                "-v", f"{self.SET[self.source]}:/ext/fs-subjects",
                "-e", "FS_LICENSE=license.txt",
                "1b0f81a8cb9f",
                "sh", "freesurfer.sh", function, str(start), str(end)
            ]
            # command = _command_function(max_number) + [function, str(start), str(end)]

            with open(f"{logf}/edoardo_freesurfer_{max_number}.txt", "w") as f:
                subprocess.Popen(command, stdout=f, stderr=f)

            start = end

        with open(log_file, "a") as log:
            log.write(f"with command: sh freesurfer.sh {function} {str(start)} {str(end)} >/dev/null 2>&1\n")
            log.write(f"repetitions per loop: {per_loop} \n")
            log.write("\n\n")
            
        print("")

    def debugging_container(self, function, log_file="log.txt"):
        
        
        # TODO: add check on source and destination
        logf = os.path.join(self.SET["base_path"], "docker_logs")
        if not os.path.exists(logf):
            os.makedirs(logf)

        container_list = subprocess.check_output("docker container ls --format '{{.Names}}' | grep '^edoardo_freesurfer_'", shell=True).decode().splitlines()

        max_number = 0
        for container in container_list:
            number = int(container.split("_")[-1])
            if number > max_number:
                max_number = number

        with open(log_file, "a") as log:
            log.write(f"on {datetime.now()} containers started: \n")

        max_number += 1

        print(f"running container edoardo_freesurfer_{max_number}")
        # print(f"with parameters sh freesurfer.sh {function} {start} {end}")

        with open(log_file, "a") as log:
            log.write(f"    edoardo_freesurfer_{max_number}\n")

        command = [ # " ".join(
            "docker", "run", "--rm", "--name", f"edoardo_freesurfer_{max_number}",
            "-v", f"{self.SET["license_path"]}:/license.txt:ro",
            "-v", f"{self.SET["app_path"]}/freesurfer_all.sh:/root/freesurfer.sh",
            "-v", f"{self.SET["app_path"]}/tmp:/info:ro",
            "-v", f"{self.SET[self.destination]}:/ext/processed-subjects",
            "-v", f"{self.SET[self.source]}:/ext/fs-subjects",
            "-e", "FS_LICENSE=license.txt",
            "1b0f81a8cb9f",
            "sh", "freesurfer.sh", function
        ]
        # command = _command_function(max_number) + [function]

        # with open(f"{logf}/edoardo_freesurfer_{max_number}.txt", "w") as f:
        subprocess.Popen(command)

        with open(log_file, "a") as log:
            log.write(f"with command: sh freesurfer.sh {function} >/dev/null 2>&1\n")
            log.write("\n\n")
            
        print("")
