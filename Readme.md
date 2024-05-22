
Tool to simplify the automation of freesurfer using docker on a server
### Introduction

### Preparation 
This can work on any folder, what needs to be written ever time is a funtion to find the subject name in the directory tree every time an mri is found. it can be a directory level, a part of the directory name, anthing. The mri that have the same subject name are put togehter and are considered as from the same subject. 


### Commands 

 - table (tablenifti)
 To run first you need to run create table, it can be either done starting from nifti or from dicom, default is starting from dicom, when you want to start from nifti you need to use the command tablenifti. 
 This creates a table that contains all the info on the subjects ordered in these columns: 
 ID, mris, paths. 
 Then all of these data are completed 
 - samseg
 - convert
 - register
 - fstables


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




