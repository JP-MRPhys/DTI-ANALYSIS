#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 15:16:56 2017
@author: Jehill Parikh
Requirements: NYPYPE, FSL,SPM, ANT
"""

"""
===================
dMRI: Preprocessing and TBSS analyis 
===================
Introduction
============
This script, demonstrates how to prepare dMRI data
for tractography and connectivity analysis with nipype.

Can be executed in command line using ``python "yourScript_filename".py``
Import necessary modules from nipype.
"""

import os  # system functions
import nipype.interfaces.io as nio  # Data i/o
import nipype.interfaces.utility as niu  # utility
import nipype.algorithms.misc as misc
import nipype.pipeline.engine as pe  # pypeline engine
from nipype.interfaces import fsl
from nipype.interfaces import ants
from nipype.workflows.dmri.fsl.artifacts import all_fsl_pipeline, remove_bias
from nipype.workflows.dmri.fsl.tbss import create_tbss_non_FA, create_tbss_all

# Set the subject identifier in subject_list,

subject_list = ['COGPBC2001', 'COGPBC2002', 'COGPBC2003', 'COGPBC2004', 'COGPBC2006', 'COGPBC2007', 'COGPBC2008',
                'COGPBC2009', 'COGPBC2012', 'COGPBC2013', 'COGPBC2014', 'COGPBC2015', 'COGPBC2017', 'COGPBC2018',
                'COGPBC2019', 'COGPBC2020', 'COGPBC2021', 'COGPBC2023', 'COGPBC2025']

# set the data directories
dataDir = os.path.abspath('/home/jehill/mriarchive/COGPBC2/NIFTI_data/')
resultsDir = os.path.abspath('/home/jehill/mriarchive/COGPBC2/DTI_analysis/DTI_FIT/')
preprocessing_dir = os.path.abspath('/home/jehill/mriarchive/COGPBC2/DTI_analysis/preprocessing/')
tbss_dir = os.path.abspath('/home/jehill/mriarchive/COGPBC2/DTI_analysis/tbss/')

data = pe.Node(nio.DataGrabber(infields=['subject_id'],
                               outfields=['dwi', 'bvecs', 'bvals', 'dwi_rev']), name='datasource')
data.inputs.template = '*'
data.inputs.base_directory = dataDir
data.inputs.sort_filelist = True
data.inputs.template_args = {'dwi': [['subject_id', 'subject_id']],
                             'dwi_rev': [['subject_id', 'subject_id']],
                             'bvals': [['subject_id', 'subject_id']],
                             'bvecs': [['subject_id', 'subject_id']]}

# change the fields for the filename template to ensure that all relevant data are there in the files

data.inputs.field_template = {'dwi': '%s/%s_DT.nii',
                              'dwi_rev': '%s/%s_DT_flip.nii',
                              'bvals': '%s/%s.bval',
                              'bvecs': '%s/%s.bvec'}

# this is where the output of the pre-process will be store
# Update we would just store the run FDT in a directory
# run TBSS later using this as the input of the data for FA maps for TBSS

datasink = pe.Node(interface=nio.DataSink(), name='datasink')
datasink.inputs.base_directory = resultsDir
# Define substitution strings
"""substitutions = [('_task-flanker', ''),
                 ('_bold_mcf', ''),
                 ('.nii.gz_mean_reg', '_mean'),
                 ('.nii.gz.par', '.par')]
datasink.inputs.substitutions = substitutions


"""

# datasource.inputs.template_args = info

# Using the IdentityInterface
from nipype import IdentityInterface

infosource = pe.Node(IdentityInterface(fields=['subject_id']), name="infosource")
infosource.iterables = [('subject_id', subject_list)]

"""
Setup for dMRI preprocessing
============================
In this section we initialize the appropriate workflow for preprocessing of
diffusion images.

Artifacts correction
--------------------
We will use the combination of ``topup`` and ``eddy`` as suggested by FSL.
In order to configure the susceptibility distortion correction (SDC), we first
write the specific parameters our echo-planar imaging (EPI) images.

Particularly, we look into the ``acqparams.txt`` file of the selected subject
to gather the encoding direction, acceleration factor (in parallel sequences
it is > 1), and readout time or echospacing.

"""

epi_AP = {'echospacing': 66.5e-3, 'enc_dir': 'y-'}
epi_PA = {'echospacing': 66.5e-3, 'enc_dir': 'y'}
prep = all_fsl_pipeline(epi_params=epi_AP, altepi_params=epi_PA)

"""
Bias field correction
---------------------
Finally, we set up a node to correct for a single multiplicative bias field
from computed on the *b0* image, as suggested in [Jeurissen2014]_.
"""

bias = remove_bias()

"""
Now run the DTI fit on them
"""
dtifit = pe.Node(interface=fsl.DTIFit(), name='dtifit')

"""
Connect nodes in workflow
=========================
We create a higher level workflow to connect the nodes. Please excuse the
author for writing the arguments of the ``connect`` function in a not-standard
style with readability aims.
"""

wf = pe.Workflow(name="diffussion_preprocessing")
wf.base_dir = preprocessing_dir
wf.connect([

    # pass the the subject list
    (infosource, data, [('subject_id', 'subject_id')]),

    # do the preproecssing eddy and top up
    (data, prep, [('dwi', 'inputnode.in_file'),
                  ('dwi_rev', 'inputnode.alt_file'),
                  ('bvals', 'inputnode.in_bval'),
                  ('bvecs', 'inputnode.in_bvec')]),

    # do the bias correction

    (prep, bias, [('outputnode.out_file', 'inputnode.in_file'),
                  ('outputnode.out_mask', 'inputnode.in_mask')]),

    (data, bias, [('bvals', 'inputnode.in_bval')]),

    # rund dtifit

    (infosource, dtifit, [('subject_id', 'base_name')]),

    (data, dtifit, [('bvals', 'bvals'),
                    ('bvecs', 'bvecs')]),

    (prep, dtifit, [('outputnode.out_file', 'dwi'),
                    ('outputnode.out_mask', 'mask')]),

    # copy of the data using data sink
    # raw inputs are already present so we won't copy them
    # bet, top and eddy current file
    (prep, datasink, [('fsl_eddy.out_corrected', 'results.@DWI_eddy_corrected_output'),
                      ('bet_dwi_post.mask_file', 'results.@bet_mask_post_eddy')]),
    # ('topup.out_corrected', 'results.@top') ]),

    #
    (dtifit, datasink, [('FA', 'results.@FA'),
                        ('MD', 'results.@MD')])

])

# to add the sinker to sort the data
# (prep,datasink1, [('outputnode.out_mask'),'preproc.@' ]), #write the EDDY current data

# now the TBSS analysis

tbss_source = pe.Node(
    interface=nio.DataGrabber(outfiles=['fa_list', 'md_list']),
    name='tbss_source')
tbss_source.inputs.base_directory = datasink.inputs.base_directory
tbss_source.inputs.template = '%s/%s_%s.nii'
tbss_source.inputs.template_args = dict(
    fa_list=[['FA', subject_list, 'FA']],
    md_list=[['MD', subject_list, 'MD']])
tbss_source.inputs.sort_filelist = True

"""
TBSS analysis
"""

tbss_all = create_tbss_all()
tbss_all.inputs.inputnode.skeleton_thresh = 0.2

tbssproc = pe.Workflow(name="tbssproc")
tbssproc.base_dir = tbss_dir  # os.path.join(os.path.abspath(resultsDir), ,'tbss', 'l2')
tbssproc.connect(tbss_source, 'fa_list', tbss_all, 'inputnode.fa_list')

tbss_MD = create_tbss_non_FA(name='tbss_MD')
tbss_MD.inputs.inputnode.skeleton_thresh = tbss_all.inputs.inputnode.skeleton_thresh

tbssproc.connect([
    (tbss_all, tbss_MD,
     [('tbss2.outputnode.field_list', 'inputnode.field_list'),
      ('tbss3.outputnode.groupmask', 'inputnode.groupmask'),
      ('tbss3.outputnode.meanfa_file',
       'inputnode.meanfa_file'), ('tbss4.outputnode.distance_map',
                                  'inputnode.distance_map')]),
    (tbss_source, tbss_MD, [('md_list', 'inputnode.file_list')]),
])

"""
Run the workflow as command line executable
"""

if __name__ == '__main__':
    # do the preprocessing
    wf.run()
    wf.write_graph()

    # do the DTI analysis
    tbssproc.run()  # do the TBSS
    tbssproc.write_graph()
