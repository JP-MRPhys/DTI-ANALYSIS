# Pipeline to do advanced DTI pre-processing and Tractography analysis 

##Requirement 
  1. Packages: NIPYPE, FSL, DICOM2NIFTI, ANTS, SPM (MATLAB)
  2. Configuration: Anaconda
  3. DTI data (with flipped B0 acquistions to apply eddy current corrections)
  
  
  ##Stage 1. 
  
  Preprocessing (top-up and eddy current), DTI-FIT to generate FA and MD data using DTI scan, BVEC, BVALS, DTI_Bo_flipped (eddy     current correction) 
  
  ##Stage 2 
  
  Using FA and MD values to do track based spatial stastistics (TBSS)
  
  ##Stage 3 (Not part of this script)
  
  Trackvis: To do visulisation and isoloation of tracks
 
# Usage
Change the directories, and subject_list and filename template as per your data 
then run the scripts python "yourfilename.py"
