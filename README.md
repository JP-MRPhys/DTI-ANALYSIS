## Pipeline to do advanced duffsion tensor image analysis, pre-processing, track based spatial statistics (TBSS) and tract visualisation  


### Example image (low resolution)
![dti1](https://user-images.githubusercontent.com/10104388/43639024-bd1bcfc8-9712-11e8-8181-1cfca7205d4d.png)

## Requirement 
  1. Packages: NIPYPE, FSL, DICOM2NIFTI, ANTS, SPM (MATLAB)
  2. Configuration: Anaconda
  3. DTI scan, b-vectors and b-values files, and flipped B0 acquistions to apply eddy current corrections
  
  
  ## Stage 1 (PREPROCESSING)
  
  Preprocessing (top-up and eddy current), DTI-FIT to generate FA and MD data using DTI scan, BVEC, BVALS, DTI_Bo_flipped (eddy     current correction) 
  
  ## Stage 2 (TBSS)
  
  Using FA and MD values to do track based spatial stastistics (TBSS)
  
  ## Stage 3 (Track Isolation: Not part of this script)
  
  Trackvis: To do visulisation and isolation of individual tracks
 
  ## Usage
  
  Change the directories, and subject_list and filename template as per your data 
  then run the script in terminal (and see if after are fews days) 
  
  python "yourfilename.py"
  
  ### WIP 
  
  1. Difussion kurtosis imaging 
  2. GPU support for eddy and DTI-FIT


