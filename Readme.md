
Tool to simplify the automation of freesurfer using docker on a server
### Introduction


### Functionalities

- Prepare dicom: given the "dicom_raw" folder, defined in settings, convert the folder in a usable structure and saves it in "dicom": 
    in a usable folder all the dicom folders are at the first level, 
    The default function works with second level dicom (each subjkect has multiple acquistions with multiple files), and saves a data structure in which 
    for each acquisition a new folder is created
    For other strutures it needs to be modified

- create_table: 
    creates a table with the subjects information. this step is needed for the rest of the processing
    as the code reads it every time
    the location is saved in the settings as table_location 
    the way it saves the subject name and the mri name also needs to be changed when needed. For now it combines the two first two levels after the dicom. the dicom foler becomes the mriname (which will be the nifti name)
    It also checks wether it is possible to run samseg and reconall

- convert dicom: converts the dicom folder in nifti, only T1, T2 or NIFTI, this can also be modified
    The results are saved in the folder named "nifti" and the origin is "dicom" in the settings
    source folder "dicom"
    destination folder "nifit"


- run recon all: 
    Recon all is run on the T1 present, only once per subject (or acquisition) 

    source folder "nifti"
    destination folder "reconall"

- registration 
    T2 and T1 are coregistered to run samseg. 

- samseg 
    Runs the samseg on T1 and T2

    source folder "dicom"
    destination folder "samseg"


#### Workflow example: 
    install softweare runnning install.sh
    set in settings the parameters and the substrings to to check for matching
    run prepare dicom on the raw folder (can also be external or tmp)
    create the table
    run convert nifti 
    run reconall 
        or 
    run registration 
    run samseg

### Configuration File Description
What is it?

#### Paths

- **nifti**: The path to the directory containing NIfTI files.
- **base_path**: The base directory path for various tools and outputs.
- **dicom**: The path to the directory containing DICOM files.
- **app_path**: The path to the application directory.
- **reconall**: The path to the directory for recon-all results.
- **samseg**: The path to the directory for SAMSEG results.
- **license_path**: The path to the license file.
- **table_path**: The path to the directory for table results.
- **table_name**: The name of the table file.

#### File Identifiers

- **file_identifiers**: A dictionary containing identifiers for different types of MRI files.
  - **T1**: Identifiers for T1 MRI files.
  - **T2**: Identifiers for T2 MRI files.
  - **FLAIR**: Identifiers for FLAIR MRI files.
  - **T1_no**: Identifiers for files that are not T1 MRI (selection by exclusion).
  - **T2_no**: Identifiers for files that are not T2 MRI.
  - **FLAIR_no**: Identifiers for files that are not FLAIR MRI.
