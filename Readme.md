### Configuration File Description

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
