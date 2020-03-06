#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:24:43 2020

@author: root
"""
#----------------------Commands to test 

"""list_subjs = ["sub-17589","sub-41064","sub-42173","sub-42479","sub-42525","sub-42725","sub-43352","sub-43583","sub-43605","sub-43852",
            "sub-44574","sub-44688","sub-45274"]"""

list_subjs = ["sub-42173", "sub-42525"]

for subject_id in list_subjs:
    #defines WF
    fmri2t1_wf=get_fmri2standard_wf([10,500], subject_id, '/home/mariacabello/git_projects/MRI_preprocess/acparams_hcp.txt')
    
    fmri2t1_wf.base_dir='/home/mariacabello/wf_workspace/OUTPUT_fmri2standard'
    
    #sets necessary inputs
    fmri2t1_wf.inputs.input_node.T1_img = '/institut/processed_data/BBHI_func/{subject_id}/ses-01/anat/{subject_id}_ses-01_run-01_T1w.nii.gz'.format(subject_id=subject_id)
    fmri2t1_wf.inputs.input_node.func_bold_ap_img = '/institut/processed_data/BBHI_func/{subject_id}/ses-01/func/{subject_id}_ses-01_run-01_rest_bold_ap.nii.gz'.format(subject_id=subject_id)
    fmri2t1_wf.inputs.input_node.func_sbref_img = '/institut/processed_data/BBHI_func/{subject_id}/ses-01/func/{subject_id}_ses-01_run-01_rest_sbref_ap.nii.gz'.format(subject_id=subject_id)
    fmri2t1_wf.inputs.input_node.func_segfm_ap_img = '/institut/processed_data/BBHI_func/{subject_id}/ses-01/func/{subject_id}_ses-01_run-01_rest_sefm_ap.nii.gz'.format(subject_id=subject_id)
    fmri2t1_wf.inputs.input_node.func_segfm_pa_img = '/institut/processed_data/BBHI_func/{subject_id}/ses-01/func/{subject_id}_ses-01_run-01_rest_sefm_pa.nii.gz'.format(subject_id=subject_id)
    fmri2t1_wf.inputs.input_node.T1_brain_freesurfer_mask = '/institut/processed_data/BBHI_output/structural/{subject_id}/mri/brainmask.mgz'.format(subject_id=subject_id)
    
    #writes WF graph and runs it
    #fmri2t1_wf.write_graph()
    fmri2t1_wf.run()




# PROBANDO

import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import cv2

timeseries_file='/home/mariacabello/wf_workspace/fmri2standard/apply_topup/sub-41064_ses-01_run-01_rest_bold_ap_roi_mcf_corrected.nii.gz'
sb_ref_file='/home/mariacabello/wf_workspace/fmri2standard/Topup_SEgfm_estimation/sub-41064_ses-01_run-01_rest_sefm_ap_merged_corrected.nii.gz'
label_file='/institut/processed_data/BBHI_output/structural/sub-41064/mri/aseg.mgz'
epi2reg='/home/mariacabello/wf_workspace/fmri2standard/epi2reg/SEgfm2T1.mat'

aseg = nib.load(label_file)
sbref = nib.load(sb_ref_file)
aseg_data = aseg.get_fdata()
aseg2_data = aseg_data.copy()
aseg2_data[((aseg_data!=2)*(aseg_data!=41))] = 0
aseg2_data[aseg2_data>0]=1

#load epi2reg
epi2reg=np.loadtxt(epi2reg)

#Voxel_aseg --> Voxel_epi transform
VT12Vepi_transform=np.matmul(np.linalg.inv(sbref.affine),np.matmul(np.linalg.inv(epi2reg),aseg.affine))


VT12Vepi_transform.dot([155,152,199,1])

coords = np.array(np.where(aseg2_data>0))
coords=np.vstack((coords, np.ones((1,coords.shape[1]))))
VT12Vepi_transform.dot(coords)


mri_convert --in_type mgz --out_type nii /institut/processed_data/BBHI_output/structural/sub-41064/mri/brainmask.auto.mgz /home/mariacabello/wf_workspace/brain.mask.auto.nii.gz


flirt -in /home/mariacabello/wf_workspace/fmri2standard/Topup_SEgfm_estimation/sub-41064_ses-01_run-01_rest_sefm_ap_merged_corrected.nii.gz -ref /institut/processed_data/BBHI_func/sub-41064/ses-01/anat/sub-41064_ses-01_run-01_T1w.nii.gz -init /home/mariacabello/wf_workspace/fmri2standard/epi2reg/SEgfm2T1.mat

def f(i, j, k):
...    """ Return X, Y, Z coordinates for i, j, k """
...    return M.dot([i, j, k]) + abc



mri_convert /institut/processed_data/BBHI_output/structural/sub-41064/mri/aseg.mgz /home/mariacabello/wf_workspace/aseg_fmri_space.mgz -vs 2 2 2 -oni 104 -onj 104 -onk 72 --apply_transform  /home/mariacabello/wf_workspace/SEgfm2T1.xfm




kernel = np.ones((2,2), np.uint8) 

aseg2_eroded_data = cv2.erode(aseg2_data, kernel, iterations=1) 

show_slices([aseg2_eroded_data[100, :, :],
             aseg2_data[:,100,:],
             aseg2_data[:, :, 100]])

indices: a list of indices for ROIs to extract.