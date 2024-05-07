
count=0

VOLUMES_DIR=/ext/fs-subjects
export FREESURFER_HOME=/usr/local/freesurfer
export SUBJECTS_DIR=/ext/processed-subjects 
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export FS_LICENSE=/license.txt

cd $VOLUMES_DIR

start=0
end=1

test=0

create_tables() {

  cd $SUBJECTS_DIR
  asegstats2table --subjectsfile $subjects_path --meas volume --tablefile aseg_volumes.txt --skip

  aparcstats2table --subjectsfile $subjects_path --hemi rh --meas thickness --tablefile rh_aparc_thickness.txt --skip
  aparcstats2table --subjectsfile $subjects_path --hemi lh --meas thickness --tablefile lh_aparc_thickness.txt --skip

  aparcstats2table --subjectsfile $subjects_path --hemi rh --meas volume --tablefile rh_aparc_volume.txt --skip
  aparcstats2table --subjectsfile $subjects_path --hemi lh --meas volume --tablefile lh_aparc_volume.txt --skip

  aparcstats2table --subjectsfile $subjects_path --hemi rh --tablefile rh_aparc_area.txt --skip
  aparcstats2table --subjectsfile $subjects_path --hemi lh --tablefile lh_aparc_area.txt --skip

  # asegstats2table --statsfile hipposubfields.lh.T1.v22.stats --subjectsfile $subjects_path --tablefile hipposubfields.lh.T1.txt --skip
  # asegstats2table --statsfile hipposubfields.rh.T1.v22.stats --subjectsfile $subjects_path --tablefile hipposubfields.rh.T1.txt --skip

  # thalamus
  # asegstats2table --statsfile thalamic-nuclei.lh.v13.T1.stats --subjectsfile $subjects_path --tablefile thalamic-nuclei.lh.T1.txt
  # asegstats2table --statsfile thalamic-nuclei.rh.v13.T1.stats --subjectsfile $subjects_path --tablefile thalamic-nuclei.rh.T1.txt

  # asegstats2table --statsfile brainstem.v13.stats --subjectsfile $subjects_path --tablefile brainstem.txt --skip
}

reconall() {

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
      if [ $test -eq 0 ]; then
        recon-all -all -s $destination_filename -i $nii_volume -no-isrunning
      else  
        echo "recon-all -all -s $destination_filename -i $nii_volume -no-isrunning " > $SUBJECTS_DIR/$destination_filename.txt
      fi

      echo "running recon-all: $destination_filename... from $nii_volume"
      
      # recon-all -all -s $destination_filename -i $nii_volume -no-isrunning 
      # recon-all -autorecon2-wm  -s $destination_filename -i $nii_volume -no-isrunning -nofix
      
      # sleep 1

      echo "done"
      
    fi
    
    if [ $count -ge $end ]; then
        echo "stopped at iteration $count"
        break
    fi
  done

}

samseg() {
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

      if [ $test -eq 0 ]; then
        run_samseg --input "$t1" "$t2_flair"  --pallidum-separate --output "$SUBJECTS_DIR/$folder" --lesion --threads 8
      else  
        echo "run_samseg --input "$t1" "$t2_flair"  --pallidum-separate --output "$SUBJECTS_DIR/$folder" --lesion --threads 8" > $SUBJECTS_DIR/$folder.txt
      fi

      echo "done"
      
    fi
    
    if [ $count -ge $end ]; then
        echo "stopped at iteration $count"
        break
    fi
  done
}

register(){
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
            


      if [ $test -eq 0 ]; then
        echo "running coreg..."  
        mri_coreg --mov $t2_flair --ref $t1 --reg "$folder/$registration_name" >/dev/null 
        echo "coreg OK - running vol2vol..."
        mri_vol2vol --mov  $t2_flair  --reg "$folder/$registration_name"  --o "$folder/$registered_flair_name" --targ $t1 >/dev/null 
        echo "vol2vol OK"
        echo "done subject: $count - $folder"
      else  
        echo "running coreg..."  
        echo "mri_coreg --mov $t2_flair --ref $t1 --reg $folder/$registration_nam "  > $SUBJECTS_DIR/$folder/$registration_name.txt
        echo "coreg OK - running vol2vol..."
        echo "mri_vol2vol --mov  $t2_flair  --reg $folder/$registration_name  --o $folder/$registered_flair_name --targ $t1 " > $SUBJECTS_DIR/$folder/$registered_flair_name.txt
        echo "vol2vol OK"
        echo "done subject: $count - $folder"
      fi

    fi
  
    if [ $count -ge $end ]; then
        echo "stopped at iteration $count"
        break
    fi
  done
}

convertdicom(){
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
      

      if [ $test -eq 0 ]; then
        mri_convert "$dicom_folder/$first_element" "$destination_filename" #>/dev/null 
      else  
        echo "mri_convert $dicom_folder/$first_element $destination_filename "  > $SUBJECTS_DIR/$dir.txt
      fi     
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
