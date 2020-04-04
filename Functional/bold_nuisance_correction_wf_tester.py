#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  23 13:05:43 2020

@author: María Cabello
"""
#----------------------Commands to test 


from fmri_nuisance_correction import get_nuisance_regressors_wf
from nipype.interfaces.fsl.utils import ImageMeants
import os

root_path = '/home/mariacabello/wf_workspace/thesis_data'
heudiconv_folder='func_anat'
fmri2standard_folder='fmri2standard'
fmri2standard_path=root_path+'/'+fmri2standard_folder
nuisance_correction_path=root_path+'/nuisance_correction'

all_subjects = [f for f in os.listdir(fmri2standard_path) if os.path.isdir(os.path.join(fmri2standard_path, f)) and f.find("sub-")!=-1]
done_subjects = [f for f in os.listdir(nuisance_correction_path) if os.path.isdir(os.path.join(nuisance_correction_path, f)) and f.find("sub-")!=-1]

list_subjs=set(all_subjects).difference(set(done_subjects))


list_subjs = [
#        "sub-103151", 
#        "sub-116245","sub-129073","sub-151965","sub-161022",
#         #"sub-184420", ¿?¿?¿? NO BOLD
#        "sub-185225","sub-187232",
        "sub-48296",
        "sub-49664",
        "sub-50000","sub-73417","sub-84766","sub-86143","sub-88604",
        "sub-92889","sub-92918","sub-93338"
        ]

#extracting timesieries
extraction = ImageMeants()

for subject_id in list_subjs:
    #defines WF
    wf_reg=get_nuisance_regressors_wf(outdir=root_path+'/nuisance_correction', subject_id=subject_id, timepoints=490)

    #sets necessary inputs
    wf_reg.inputs.input_node.realign_movpar_txt = root_path+'/fmri2standard/{subject_id}/realign_fmri2SBref/{subject_id}_ses-01_run-01_rest_bold_ap_roi_mcf.nii.gz.par'.format(subject_id=subject_id)    
    wf_reg.inputs.input_node.rfmri_unwarped_imgs = root_path+'/fmri2standard/{subject_id}/spm_coregister2T1_bold/{subject_id}_ses-01_run-01_rest_bold_ap_roi_mcf_corrected_coregistered2T1.nii.gz'.format(subject_id=subject_id)
    #wf_reg.inputs.input_node.masks_imgs = root_path+'/nuisance_correction/{subject_id}/masks_csf_wm/wm_binmask.nii.gz'.format(subject_id=subject_id)
    wf_reg.inputs.input_node.mask_wm = root_path+'/nuisance_correction/{subject_id}/masks_csf_wm/wm_binmask.nii.gz'.format(subject_id=subject_id)
    wf_reg.inputs.input_node.mask_csf = root_path+'/nuisance_correction/{subject_id}/masks_csf_wm/csf_binmask.nii.gz'.format(subject_id=subject_id)
    #CONNECT WITH fmri2standard WF  
    wf_reg.inputs.input_node.bold_img = root_path+'/fmri2standard/{subject_id}/spm_coregister2T1_bold/{subject_id}_ses-01_run-01_rest_bold_ap_roi_mcf_corrected_coregistered2T1.nii.gz'.format(subject_id=subject_id)
    
    #writes WF graph and runs it
    #wf_reg.write_graph()
    #wf_reg.run()
    
    print("Extracting...")
    extraction.inputs.in_file=root_path+'/nuisance_correction/{subject_id}/filter_regressors_bold/{subject_id}_ses-01_run-01_rest_bold_ap_roi_mcf_corrected_coregistered2T1_regfilt.nii.gz'.format(subject_id=subject_id)
    extraction.inputs.out_file=root_path+'/timeseries/{subject_id}/{subject_id}_ses-01_run-01_rest_bold_glasser_timeseries.txt'.format(subject_id=subject_id)
    #extraction.inputs.out_file=root_path+'/timeseries/{subject_id}/{subject_id}_ses-01_run-01_rest_bold_glasser_timeseries_leftV1.txt'.format(subject_id=subject_id)
    
    extraction.inputs.mask=root_path+'/glasser/{subject_id}/glasser_volumetric_T1_boldT1.nii.gz'.format(subject_id=subject_id)
    #extraction.inputs.mask=root_path+'/glasser/{subject_id}/left_V1_mask.nii.gz'.format(subject_id=subject_id)
    
    extraction.run()