import subprocess
import datetime 
import helper_functions as h

SET = h.load_settings("settings.json")

class DockerInstance():
    def __init__(self, SET, source, destination):
        self.source = source
        self.destination = destination
        self.SET = SET

    def run(self, function, n_loops, per_loop, log_file="log.txt"):
        
        # TODO: add check on source and destination

        start = 0
        print(f"Total containers to be run {n_loops + 1}")
        container_list = subprocess.check_output("docker container ls --format '{{.Names}}' | grep '^edoardo_freesurfer_'", shell=True).decode().splitlines()

        max_number = 0
        for container in container_list:
            number = int(container.split("_")[-1])
            if number > max_number:
                max_number = number

        with open(log_file, "a") as log:
            log.write(f"on {datetime.now()} containers started: \n")

        for i in range(n_loops):
            end = start + per_loop
            max_number += 1
            print(f"Iteration: {i+1}")
            print(f"running container edoardo_freesurfer_{max_number}")
            print(f"with parameters sh freesurfer.sh {function} {start} {end}")

            with open(log_file, "a") as log:
                log.write(f"    edoardo_freesurfer_{max_number}\n")

            command = [
                "docker", "run", "--rm", "--name", f"edoardo_freesurfer_{max_number}",
                "-v", f"{SET["base_path"]}/license.txt:/license.txt:ro",
                "-v", f"{SET["base_path"]}/freesurfer_all.sh:/root/freesurfer.sh",
                "-v", f"{SET["base_path"]}:{SET["base_path"]}:ro",
                "-v", f"{SET[self.source]}:",
                "-v", f"{SET[self.destination]}:",
                "-e", "FS_LICENSE=license.txt",
                "1b0f81a8cb9f",
                "sh", "freesurfer.sh", function, str(start), str(end)
            ]
                
            subprocess.Popen(command, shell=True)

            start = end

        with open(log_file, "a") as log:
            log.write(f"with command: sh freesurfer.sh {function} >/dev/null 2>&1\n")
            log.write(f"repetitions per loop: {per_loop} \n")
            log.write("\n\n")

    def debugging_container(self, function):
        pass