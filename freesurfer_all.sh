
count=0

VOLUMES_DIR=/ext/fs-subjects
export FREESURFER_HOME=/usr/local/freesurfer
export SUBJECTS_DIR=/ext/processed-subjects 
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export FS_LICENSE=/license.txt

cd $VOLUMES_DIR

start=0
end=1
dcm2niix -o /path/to/output/folder -f desired_name /path/to/dicom/folder

# convert samseg segmentation to nifti
iterate_convert_dicom_dicom2niix(){
  for dicom_folder in "${origins[@]}"; do

    dir="$(dirname ${destinations[count]})" 
    destination_filename="${destinations[count]}"
    count=$((count + 1)) 
    
    if [ $count -ge $start ]; then
    
      echo " "
      echo "subject: $count - $destination_filename"
      
      if [ -f "$destination_filename" ]; then
        echo "Skipping $destination_filename - Already processed"
        continue  # Skip to the next iteration
      fi
            
      first_element=$(ls $dicom_folder | head -1)
      
      echo "dcm2niix -o $destination_filename -f $dir $dicom_folder"
      
      mkdir $dir
      # mri_convert "$dicom_folder/$first_element" "$destination_filename" #>/dev/null      
      dcm2niix -o $destination_filename -f $dir $dicom_folder

      echo "done"
      
    fi
    
    if [ $count -ge $end ]; then
        echo "stopped at iteration $count"
        break
    fi
  done
}
# convert samseg segmentation to nifti
s_to_n() {
  # put as origin: amseg_result_lesions
  # put as destination # samseg_result_lesions

  # Iterate through the array using a for loop
  for subject in "${origins[@]}"; do
  
    # subject="${destinations[count]}"
    count=$((count + 1)) 
    
    if [ $count -ge $start ]; then
    
    
      echo "mri_convert $subject/seg.mgz $subject/seg.nii"      

      mri_convert $subject/seg.mgz $subject/seg.nii


      echo "done"
      
    fi
    
    if [ $count -ge $end ]; then
        echo "stopped at iteration $count"
        break
    fi
  done
}

crop_for_network() {
  # put as origin: MRI_converted_nifti 
  # put as destination # reconall_results
  cd $VOLUMES_DIR

  # Iterate through the array using a for loop
  for subject in "${origins[@]}"; do
  
    # subject="${destinations[count]}"
    count=$((count + 1)) 
    
    if [ $count -ge $start ]; then
    
    
      echo "mri_convert $subject/mask.nii --cropsize 160 214 176 $subject/cropped_mask.nii"      

      mri_convert $subject/aseg+aparc_binary_mask.nii --cropsize 214 160 176 $subject/cropped_mask_swapped.nii
      mri_convert $subject/t1_rescaled.nii --cropsize 214 160 176 $subject/cropped_t1_swapped.nii
      mri_convert $subject/_flair_reg.nii --cropsize 214 160 176 $subject/cropped_flair_swapped.nii

      echo "done"
      
    fi
    
    if [ $count -ge $end ]; then
        echo "stopped at iteration $count"
        break
    fi
  done
}

prepare_for_network() {
  # put as origin: MRI_converted_nifti 
  # put as destination # reconall_results

  # Iterate through the array using a for loop
  for subject in "${origins[@]}"; do
  
    # subject="${destinations[count]}"
    count=$((count + 1)) 
    
    if [ $count -ge $start ]; then
    
      # pwi
      echo "mri_vol2vol --mov $subject/mri/aparc+aseg.mgz --targ $subject/mri/orig/001.mgz --regheader --o $SUBJECTS_DIR/$subject/aparc+aseg_origspace.mgz --no-save-reg"      


      mri_vol2vol --mov $subject/mri/aparc+aseg.mgz --targ $subject/mri/orig/001.mgz --regheader --o $SUBJECTS_DIR/$subject/aparc+aseg_origspace.mgz --no-save-reg
      echo "done"
      
    fi
    
    if [ $count -ge $end ]; then
        echo "stopped at iteration $count"
        break
    fi
  done
}

create_tables() {

  cd $SUBJECTS_DIR
  asegstats2table --subjectsfile $subjects_path --meas volume --tablefile aseg_volumes.txt --skip

  aparcstats2table --subjectsfile $subjects_path --hemi rh --meas thickness --tablefile rh_aparc_thickness.txt --skip
  aparcstats2table --subjectsfile $subjects_path --hemi lh --meas thickness --tablefile lh_aparc_thickness.txt --skip

  aparcstats2table --subjectsfile $subjects_path --hemi rh --meas volume --tablefile rh_aparc_volume.txt --skip
  aparcstats2table --subjectsfile $subjects_path --hemi lh --meas volume --tablefile lh_aparc_volume.txt --skip

  asegstats2table --statsfile hipposubfields.lh.T1.v22.stats --subjectsfile $subjects_path --tablefile hipposubfields.lh.T1.txt --skip
  asegstats2table --statsfile hipposubfields.rh.T1.v22.stats --subjectsfile $subjects_path --tablefile hipposubfields.rh.T1.txt --skip

  # thalamus
  asegstats2table --statsfile thalamic-nuclei.lh.v13.T1.stats --subjectsfile $subjects_path --tablefile thalamic-nuclei.lh.T1.txt
  asegstats2table --statsfile thalamic-nuclei.rh.v13.T1.stats --subjectsfile $subjects_path --tablefile thalamic-nuclei.rh.T1.txt

  asegstats2table --statsfile brainstem.v13.stats --subjectsfile $subjects_path --tablefile brainstem.txt --skip
}

iterate_hippocampus() {

  /info/install -agreeToLicense yes

  # Iterate through the array using a for loop
  for subject in "${origins[@]}"; do
  
    # subject="${destinations[count]}"
    count=$((count + 1)) 
    
    if [ $count -ge $start ]; then
    
    
      echo "subject n $count: - $subject running segmentBS.sh segmentHA_T1.sh segmentThalamicNuclei.sh"      


      segmentBS.sh $subject
      segmentHA_T1.sh $subject
      segmentThalamicNuclei.sh  $subject
      
      echo "done"
      
    fi
    
    if [ $count -ge $end ]; then
        echo "stopped at iteration $count"
        break
    fi
  done

}

iterate_thalamus() {

  /info/install -agreeToLicense yes

  # Iterate through the array using a for loop
  for subject in "${origins[@]}"; do
  
    # destination_filename="${destinations[count]}"
    count=$((count + 1)) 
    
    if [ $count -ge $start ]; then
    
      echo " "

      echo "subject n $count: - $subject running segmentThalamicNuclei.sh"
      segmentThalamicNuclei.sh  $subject
      
      echo "done"
      
    fi
    
    if [ $count -ge $end ]; then
        echo "stopped at iteration $count"
        break
    fi
  done

}

iterate_recon_all() {

  # Iterate through the array using a for loop
  for nii_volume in "${origins[@]}"; do
  
    destination_filename="${destinations[count]}"
    count=$((count + 1)) 
    
    if [ $count -ge $start ]; then
    
      echo " "
      echo "subject: $count - $SUBJECTS_DIR/$destination_filename"
      
      # if [ -d "$SUBJECTS_DIR/$destination_filename" ]; then
        # echo "Deleting folder: $SUBJECTS_DIR/$destination_filename"
        # rm -r "$SUBJECTS_DIR/$destination_filename"
      # fi
            
      echo "running recon-all: $destination_filename... from $nii_volume"
      
      recon-all -all -s $destination_filename -i $nii_volume -no-isrunning 
      # recon-all -autorecon2-wm  -s $destination_filename -i $nii_volume -no-isrunning -nofix
      
      echo "done"
      
    fi
    
    if [ $count -ge $end ]; then
        echo "stopped at iteration $count"
        break
    fi
  done

}

iterate_samseg() {
  read_line=0
  for folder in "${destinations[@]}"; do
    count=$((count + 1)) 

    t1="${origins[read_line]}"
    read_line=$((read_line + 1)) 
    t2_flair="${origins[read_line]}"
    read_line=$((read_line + 1)) 
    
    if [ $count -ge $start ]; then
    
      echo " "
      echo "subject: $count - $folder"
      
      if [ -f "%SUBJECTS_DIR/$folder" ]; then
        echo "Skipping $folder - Already processed"
        continue  # Skip to the next iteration
      fi
            
      echo "running samseg: $SUBJECTS_DIR/$folder..."
      echo "run_samseg --input $t1 $VOLUMES_DIR/$t2_flair  --pallidum-separate"
      echo "--output $SUBJECTS_DIR/$folder --threads 8"
      
      run_samseg --input "$t1" "$t2_flair"  --pallidum-separate --output "$SUBJECTS_DIR/$folder" --lesion --threads 8 # > /dev/null

      
      echo "done"
      
    fi
    
    if [ $count -ge $end ]; then
        echo "stopped at iteration $count"
        break
    fi
  done
}

iterate_register_samseg(){
  read_line=0
  registration_name="flair_t2_ToT1.lta"
  registered_flair_name="flair_t2_reg.nii"
  for folder in "${destinations[@]}"; do
    count=$((count + 1)) 

    t1="${origins[read_line]}"
    read_line=$((read_line + 1)) 
    t2_flair="${origins[read_line]}"
    read_line=$((read_line + 1)) 
  
  
    if [ $count -ge $start ]; then
    
      echo " "
      echo "subject: $count - $folder"
      
      if [ -f "%$SUBJECTS_DIR/$folder" ]; then
        echo "Skipping $folder - Already processed"
        continue  # Skip to the next iteration
      fi
            
      echo "running coreg..."  
      mri_coreg --mov $t2_flair --ref $t1 --reg "$folder/$registration_name" >/dev/null 
      echo "coreg OK - running vol2vol..."
      mri_vol2vol --mov  $t2_flair  --reg "$folder/$registration_name"  --o "$folder/$registered_flair_name" --targ $t1 >/dev/null 
      echo "vol2vol OK"
      echo "done subject: $count - $folder"

    fi
  
    if [ $count -ge $end ]; then
        echo "stopped at iteration $count"
        break
    fi
  done
}

iterate_convert_samseg(){
  for destination_filename in "${destinations[@]}"; do

    
    dir="$(dirname ${destinations[count]})" 
    dicom_folder="${origins[count]}"
    count=$((count + 1)) 

    if [ $count -ge $start ]; then

      if [ -f "$destination_filename" ]; then
        echo "Skipping $destination_filename - Already processed"
        continue  # Skip to the next iteration
      fi

      echo " "
      echo "subject: $count - $folder"
            
      first_element=$(ls $dicom_folder | head -1)

      mkdir $dir
      mri_convert "$dicom_folder/$first_element" "$destination_filename" #>/dev/null  

    fi
    
    if [ $count -ge $end ]; then
        echo "stopped at iteration $count"
        break
    fi

  done
}

iterate_convert_dicom(){
  for dicom_folder in "${origins[@]}"; do

    dir="$(dirname ${destinations[count]})" 
    destination_filename="${destinations[count]}"
    count=$((count + 1)) 
    
    if [ $count -ge $start ]; then
    
      echo " "
      echo "subject: $count - $destination_filename"
      
      if [ -f "$destination_filename" ]; then
        echo "Skipping $destination_filename - Already processed"
        continue  # Skip to the next iteration
      fi
            
      first_element=$(ls $dicom_folder | head -1)
      
      echo "converting dicom folder: $dicom_folder..."
      
      mkdir $dir
      mri_convert "$dicom_folder/$first_element" "$destination_filename" #>/dev/null      
      
      echo "done"
      
    fi
    
    if [ $count -ge $end ]; then
        echo "stopped at iteration $count"
        break
    fi
  done
}

# python "/info/tables_processing.py"
origin_path="/info/origins.txt"
destination_path="/info/destinations.txt"
subjects_path="/info/subjects.txt"

readarray -t origins < "$origin_path"
readarray -t destinations < "$destination_path"

# Check the number of command-line arguments
if [ $# -eq 1 ]; then
  echo "You provided 1 argument: $1"
  $1
elif [ $# -eq 3 ]; then
  start=$2
  end=$3
  $1
else
    echo "Invalid number of arguments: $#. Please provide either 1 or 3 arguments."
    exit 1
fi

# iterate_convert_dicom
# iterate_thalamus
# create_tables
# iterate_samseg
# iterate_recon_all