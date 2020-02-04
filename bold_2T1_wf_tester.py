#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:24:43 2020

@author: root
"""
#----------------------Commands to test 


#defines WF
fmri2t1_wf=get_fmri2standard_wf([10,500], '/home/mariacabello/git_projects/fMRI_preprocess/acparams_hcp.txt')

fmri2t1_wf.base_dir='/home/mariacabello/wf_workspace'

#sets necessary inputs
fmri2t1_wf.inputs.input_node.T1_img = '/institut/processed_data/BBHI_func/sub-41064/ses-01/anat/sub-41064_ses-01_run-01_T1w.nii.gz'
fmri2t1_wf.inputs.input_node.func_bold_ap_img = '/institut/processed_data/BBHI_func/sub-41064/ses-01/func/sub-41064_ses-01_run-01_rest_bold_ap.nii.gz'
fmri2t1_wf.inputs.input_node.func_sbref_img = '/institut/processed_data/BBHI_func/sub-41064/ses-01/func/sub-41064_ses-01_run-01_rest_sbref_ap.nii.gz'
fmri2t1_wf.inputs.input_node.func_segfm_ap_img = '/institut/processed_data/BBHI_func/sub-41064/ses-01/func/sub-41064_ses-01_run-01_rest_sefm_ap.nii.gz'
fmri2t1_wf.inputs.input_node.func_segfm_pa_img = '/institut/processed_data/BBHI_func/sub-41064/ses-01/func/sub-41064_ses-01_run-01_rest_sefm_pa.nii.gz'

#writes WF graph or runs it
fmri2t1_wf.write_graph()
fmri2t1_wf.run()