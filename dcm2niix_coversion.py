from nipype.interfaces.dcm2nii import Dcm2niix
import os

"""
for known issue's see 
https://github.com/nipy/nipype/issues/1389

update: Nov 2018
"""

converter = Dcm2niix();


def run_conversion(converter, inputdir, output_dir):
    converter.inputs.source_dir = inputdir
    converter.inputs.compression = 5
    converter.inputs.output_dir = output_dir
    # converter.cmdline
    converter.run()


def rename_filenames(folder, subject_id):
    for filename in os.listdir(folder):
        # name = os.path.join(dirName, filename)

        print(filename)

        if ".bvec" in filename.lower():
            newfilename = subject_id + ".bvec"
            os.rename(folder + filename, folder + newfilename)

        if ".bval" in filename.lower():
            newfilename = subject_id + ".bval"
            os.rename(folder + filename, folder + newfilename)

        if ".nii.gz" in filename.lower():

            if "DT_64dirn" in filename.lower():
                newfilename = subject_id + "_DT.nii.gz"
                os.rename(folder + filename, folder + newfilename)

            if "DT_Bvalue_reverse" in filename.lower():
                newfilename = subject_id + "_DT_flip.nii.gz"
                os.rename(folder + filename, folder + newfilename)

            if "rsfMRI" in filename.lower():
                newfilename = subject_id + "_rsfMRI.nii.gz"
                os.rename(folder + filename, folder + newfilename)

            if "rsfMRI_reverse" in filename.lower():
                newfilename = subject_id + "_rsfMRI_reverse.nii.gz"
                os.rename(folder + filename, folder + newfilename)

            if "run1" in filename.lower():
                newfilename = subject_id + "_run1.nii.gz"
                os.rename(folder + filename, folder + newfilename)

            if "run2" in filename.lower():
                newfilename = subject_id + "_run2.nii.gz"
                os.rename(folder + filename, folder + newfilename)

            if "run1_reverse" in filename.lower():
                newfilename = subject_id + "_run1_reverse.nii.gz"
                os.rename(folder + filename, folder + newfilename)

            if "FLAIR" in filename.lower():
                newfilename = subject_id + "_FLAIR.nii.gz"
                os.rename(folder + filename, folder + newfilename)

            if "Survey" in filename.lower():
                newfilename = subject_id + "_SURVEY.nii.gz"
                os.rename(folder + filename, folder + newfilename)

            if "T1_TFE" in filename.lower():
                newfilename = subject_id + "_3DT1.nii.gz"
                os.rename(folder + filename, folder + newfilename)

            if "T1W_FFE" in filename.lower():
                newfilename = subject_id + "_T1w_FFE.nii.gz"
                os.rename(folder + filename, folder + newfilename)

            if "T1FA4" in filename.lower():
                newfilename = subject_id + "_DESPOT_FA4.nii.gz"
                os.rename(folder + filename, folder + newfilename)

            if "T1FA15" in filename.lower():
                newfilename = subject_id + "_DESPOT_FA15.nii.gz"
                os.rename(folder + filename, folder + newfilename)

            if "B1_map" in filename.lower():
                newfilename = subject_id + "_B1_map.nii.gz"
                os.rename(folder + filename, folder + newfilename)


if __name__ == '__main__':

    subject_list = ['COGPBC2001', 'COGPBC2002', 'COGPBC2003', 'COGPBC2004', 'COGPBC2006', 'COGPBC2007', 'COGPBC2008',
                    'COGPBC2009', 'COGPBC2012', 'COGPBC2013', 'COGPBC2014', 'COGPBC2015', 'COGPBC2017', 'COGPBC2018',
                    'COGPBC2019', 'COGPBC2020', 'COGPBC2021', 'COGPBC2023', 'COGPBC2025']

    subject_list2 = ['COGPBC2001']

    data_dir = os.path.abspath('/home/nmrc71_ubuntu/mriarchive/COGPBC2/DICOM_Data/')
    results_dir = os.path.abspath('/home/nmrc71_ubuntu/COGPBC2/NIFTI_2/')

    for subject in subject_list2:
        input_dir = os.path.join(data_dir, subject)
        output_dir = os.path.join(results_dir, subject + '/')

        os.makedir(output_dir)
        print(input_dir)
        print(output_dir)

        # run_conversion(input_dir,output_dir)
        rename_filenames(output_dir, subject)
