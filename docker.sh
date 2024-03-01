# parameters
# 1 - fucntion_name
# 2 - number of subjects to run (optional)
# 3 - number to run per container (optional)

# f5c26070586e freesurfer last 
# 09e4aa459595 other freesurfer

# available fucntions
#     create_tables
#     iterate_hippocampus
#     iterate_thalamus
#     iterate_recon_all
#     iterate_samseg
#     iterate_register_samseg
#     iterate_convert_samseg
#     iterate_convert_dicom

# to use it 
# make sure to set the correct origin and destination volumes
# run tables_processing to produce origin and destination text files correct for the use needed
# run the script in one of the two modalities
# single container -> only pass function name to be ran as argument
# multiple container -> three arguments, no output is shows and containers are created in the background
# arguments -> 
#  fucntion name 
#  number of subjects
#  subjects per container

# HOME=/mnt/S/edoardoStorage/Pipeline_MRIs

# ORIGIN=$HOME/reconall_results
# ORIGIN=/mnt/S/edoardoStorage/Pipeline_MRIs/samseg_result_lesions/
# DESTINATION=/mnt/S/edoardoStorage/Pipeline_MRIs/samseg_result_lesions/
image=1b0f81a8cb9f
HOME=/mnt/S/edoardoStorage/Pipeline_MRIs/

# ORIGIN=$HOME/reconall_results
HOME_new=/mnt/S/edoardoStorage/Pipeline_MRI2/
ORIGIN=/mnt/S/edoardoStorage/Pipeline_MRI2/PPMI_nifti/
DESTINATION=/mnt/S/edoardoStorage/Pipeline_MRI2/PPMI_nifti/

iterative_creation(){ 
  start=0
  echo "Total containers tobe run $((n_loops+1))"
  container_list=($(docker container ls --format "{{.Names}}"| grep "^edoardo_freesurfer_"))

  # Loop through the containers to find the largest number
  for container in "${container_list[@]}"; do
      number=$(echo "$container" | grep -oE '[0-9]+$') # Extract the number at the end of each container name

      if [[ $number -gt $max_number ]]; then # If the number is greater than max number, make current max number
          max_number=$number
      fi
  done
  echo "on $(date) containers started: " >> log.txt
  # Create all the containers needed (enumerate starting from max number, to mac number + n containers)
  for ((i=0; i<n_loops; i++)); do
    echo "Iteration: $((i+1))"

    end=$((start+per_loop))
    
    max_number=$((max_number+1)) # Increase max number
    echo "running container edoardo_freesurfer_$max_number" 
    echo "with parameters sh freesurfer.sh "$function" $start $end # >/dev/null 2>&1"

    echo "    edoardo_freesurfer_$max_number " >> log.txt

    docker run --rm --name edoardo_freesurfer_$max_number\
      -v $HOME/license.txt:/license.txt:ro \
      -v $HOME/freesurfer_all.sh:/root/freesurfer.sh \
      -v $SCRIPTS_OUT:$SCRIPTS_IN:ro \
      -v $FS_SUBJECT_DIR_OUT_CONTAINER:$FS_SUBJECT_DIR_IN_CONTAINER \
      -v $FS_SUBJECT_DIR_OUT_SAVE_CONTAINER:$FS_SUBJECT_DIR_IN_SAVE_CONTAINER \
      -e FS_LICENSE='license.txt' \
      1b0f81a8cb9f \
      sh freesurfer.sh "$function" $start $end # >/dev/null 2>&1 &

    echo "PID last command $!"
    start=$end

  done
  echo "with command:   sh freesurfer.sh "$function" >/dev/null 2>&1 " >> log.txt
  echo "repetitions per loop: $per_loop, total: $n_subj" >> log.txt
  echo " " >> log.txt
  echo " " >> log.txt
}

normal_creation(){ 
  #container_list=($(docker container ls --format "{{.Repository}}" | grep "^edoardo_freesurfer"))
  container_list=($(docker container ls --format "{{.Names}}"| grep "^edoardo_freesurfer_"))
  # Initialize a variable to hold the maximum number found
  max_number=0
  # echo "${container_list[@]}"
  # Loop through the containers to find the largest number
  for container in "${container_list[@]}"; do
      number=$(echo "$container" | grep -oE '[0-9]+$') # Extract the number at the end of each container name
      # echo "Extracted number from $container: $number"
      if [[ $number -gt $max_number ]]; then
          max_number=$number
      fi
  done
  max_number=$((max_number+1))
  echo "running container edoardo_freesurfer_$max_number" 
  echo "with parameters sh freesurfer.sh "$function" >/dev/null 2>&1"

  docker run -it --rm --name edoardo_freesurfer_$max_number\
    -v $HOME/license.txt:/license.txt:ro \
    -v $HOME/freesurfer_all.sh:/root/freesurfer.sh \
    -v $SCRIPTS_OUT:$SCRIPTS_IN:ro \
    -v $FS_SUBJECT_DIR_OUT_CONTAINER:$FS_SUBJECT_DIR_IN_CONTAINER \
    -v $FS_SUBJECT_DIR_OUT_SAVE_CONTAINER:$FS_SUBJECT_DIR_IN_SAVE_CONTAINER \
    -e FS_LICENSE='license.txt' \
    1b0f81a8cb9f \
    sh freesurfer.sh "$function"
    # bash
    echo "on $(date) container started: edoardo_freesurfer_$max_number with command: $function" >> log.txt
    echo " " >> log.txt
    echo " " >> log.txt
    # f5c26070586e freesurfer last 
    # 09e4aa459595 other freesurfer
}

FS_SUBJECT_DIR_OUT_CONTAINER=$ORIGIN #$1
FS_SUBJECT_DIR_IN_CONTAINER=/ext/fs-subjects 
FS_SUBJECT_DIR_OUT_SAVE_CONTAINER=$DESTINATION #$2 # for positional arguments
FS_SUBJECT_DIR_IN_SAVE_CONTAINER=/ext/processed-subjects 
SCRIPTS_OUT=$HOME_new/data_management
SCRIPTS_IN=/info


# Check the number of command-line arguments
if [ $# -eq 1 ]; then
    echo "You provided 1 argument: $1"
    function=$1
    normal_creation
elif [ $# -eq 3 ]; then
    echo "You provided 3 arguments: $1, $2, $3"
    function=$1
    n_subj=$2
    per_loop=$3
    n_loops=$((n_subj/per_loop))

    if [ $((n_subj%per_loop)) -ge 1 ]; then
      n_loops=$((n_loops + 1))
    fi
    iterative_creation
else
    echo "Invalid number of arguments. Please provide either 1 or 3 arguments."
    exit 1
fi

