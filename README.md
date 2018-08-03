# Pipeline to do advanced DTI pre-processing and Tractography analysis 

## Requirement 
  1. Packages: NIPYPE, FSL, DICOM2NIFTI, ANTS, SPM (MATLAB)
  2. Configuration: Anaconda
  3. DTI data (with flipped B0 acquistions to apply eddy current corrections)
  
  
  ## Stage 1 (PREPROCESSING)
  
  Preprocessing (top-up and eddy current), DTI-FIT to generate FA and MD data using DTI scan, BVEC, BVALS, DTI_Bo_flipped (eddy     current correction) 
  
  ## Stage 2 (TBSS)
  
  Using FA and MD values to do track based spatial stastistics (TBSS)
  
  ## Stage 3 (Track Isolation: Not part of this script)
  
  Trackvis: To do visulisation and isoloation of tracks
 
  ## Usage
  
  Change the directories, and subject_list and filename template as per your data 
  then run the script in terminal (and see if after are fews days) 
  
  python "yourfilename.py"
  
  ### WIP 
  
  1. Difussion kurtosis imaging 
  2. GPU support for eddy and DTI-FIT



