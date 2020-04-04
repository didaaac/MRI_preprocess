#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:24:43 2020

@author: root
"""
#----------------------Commands to test 


from bold2T1_wf import get_fmri2standard_wf
from nipype.interfaces import spm
import os

root_path = '/home/mariacabello/wf_workspace/thesis_data'
heudiconv_folder='func_anat'
fmri2standard_folder='fmri2standard'
bids_path=root_path+'/func_anat'
fmri2standard_path=root_path+'/'+fmri2standard_folder

all_subjects = [f for f in os.listdir(bids_path) if os.path.isdir(os.path.join(bids_path, f)) and f.find("sub-")!=-1]
done_subjects = [f for f in os.listdir(fmri2standard_path) if os.path.isdir(os.path.join(fmri2standard_path, f)) and f.find("sub-")!=-1]

list_subjs=set(all_subjects).difference(set(done_subjects))

coreg_EPI2T1 = spm.Coregister(
        # target (reference; fixed) [in .nii]
        # source (souce; moving) [in .nii]
        # apply_to_files (moving) [in .nii]
)

for subject_id in list_subjs:
    #defines WF
    fmri2t1_wf=get_fmri2standard_wf([10,500], subject_id, '/home/mariacabello/git_projects/MRI_preprocess/Functional/acparams_hcp.txt')
    
    fmri2t1_wf.base_dir=root_path+'/fmri2standard'
    
    #sets necessary inputs
    fmri2t1_wf.inputs.input_node.T1_img = bids_path+'/{subject_id}/ses-01/anat/{subject_id}_ses-01_run-01_T1w.nii.gz'.format(subject_id=subject_id)
    fmri2t1_wf.inputs.input_node.func_bold_ap_img = bids_path+'/{subject_id}/ses-01/func/{subject_id}_ses-01_run-01_rest_bold_ap.nii.gz'.format(subject_id=subject_id)
    fmri2t1_wf.inputs.input_node.func_sbref_img = bids_path+'/{subject_id}/ses-01/func/{subject_id}_ses-01_run-01_rest_sbref_ap.nii.gz'.format(subject_id=subject_id)
    fmri2t1_wf.inputs.input_node.func_segfm_ap_img = bids_path+'/{subject_id}/ses-01/func/{subject_id}_ses-01_run-01_rest_sefm_ap.nii.gz'.format(subject_id=subject_id)
    fmri2t1_wf.inputs.input_node.func_segfm_pa_img = bids_path+'/{subject_id}/ses-01/func/{subject_id}_ses-01_run-01_rest_sefm_pa.nii.gz'.format(subject_id=subject_id)
    fmri2t1_wf.inputs.input_node.T1_brain_freesurfer_mask = '/institut/processed_data/BBHI_output/structural/{subject_id}/mri/brainmask.mgz'.format(subject_id=subject_id)
    
    #writes WF graph and runs it
    #fmri2t1_wf.write_graph()
    fmri2t1_wf.run()
       

    sbref_path = root_path+'/'+fmri2standard_folder+"/{subject_id}/apply_topup_to_SBref/{subject_id}_ses-01_run-01_rest_sbref_ap_flirt_corrected_coregistered2T1.nii".format(subject_id=subject_id)
    bold_path = root_path+'/'+fmri2standard_folder+"/{subject_id}/apply_topup/{subject_id}_ses-01_run-01_rest_bold_ap_roi_mcf_corrected_coregistered2T1.nii".format(subject_id=subject_id)
       
    
    # Creating intermediate unziped .nii files
    os.system("bash intermediate-files_SPM-coregister2T1_nii-format.sh -r " + root_path + " -f " + fmri2standard_folder  + " -b " + heudiconv_folder + " -s " + subject_id + " -m to_nii")

    
    sbref2T1_path = root_path+'/'+fmri2standard_folder+"/{subject_id}/spm_coregister2T1_sbref/{subject_id}_ses-01_run-01_rest_sbref_ap_flirt_corrected_coregistered2T1.nii".format(subject_id=subject_id)
    bold2T1_path = root_path+'/'+fmri2standard_folder+"/{subject_id}/spm_coregister2T1_bold/{subject_id}_ses-01_run-01_rest_bold_ap_roi_mcf_corrected_coregistered2T1.nii".format(subject_id=subject_id)

    # SPM coregistration EPI to Standard T1
    coreg_EPI2T1.inputs.target = root_path+'/'+heudiconv_folder+'/{subject_id}/ses-01/anat/{subject_id}_ses-01_run-01_T1w.nii'.format(subject_id=subject_id)
    coreg_EPI2T1.inputs.source = sbref2T1_path
    coreg_EPI2T1.inputs.jobtype= "estimate"
    coreg_EPI2T1.inputs.apply_to_files = bold2T1_path

    coreg_EPI2T1.run()
    
    # Deleting intermediate unziped .nii files
    os.system("bash intermediate-files_SPM-coregister2T1_nii-format.sh -r " + root_path + " -f " + fmri2standard_folder  + " -b " + heudiconv_folder + " -s " + subject_id + " -m to_nii_gz")
 
    #Extracting masks from bold (wm and csf)
    sbref2T1_path=sbref2T1_path+'.gz'
    bold2T1_path=bold2T1_path+'.gz'
    output_masks = root_path+"/nuisance_correction"+"/"+subject_id+"/masks_csf_wm"
    aseg_folder = "/institut/processed_data/BBHI_output/structural/" + subject_id + "/mri/aseg.mgz"
    os.system("mkdir -p " + root_path+"/nuisance_correction"+"/"+subject_id)
    os.system("mkdir -p " + output_masks)
    os.system("bash extract_wm_csf_eroded_masks.sh -s " + subject_id + " -a " + aseg_folder  + " -r " + bold2T1_path + " -o " + output_masks + " -b " + bold2T1_path + " -e 2")
    
