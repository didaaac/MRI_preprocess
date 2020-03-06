#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:24:43 2020

@author: root
"""
#----------------------Commands to test 

from T12mni_ants_wf import get_ants_normalize_T1_MNI 

#defines WF
t12mni_wf=get_ants_normalize_T1_MNI()

t12mni_wf.base_dir='/home/mariacabello/wf_workspace'

#sets necessary inputs
t12mni_wf.inputs.input_node.T1_img = '/institut/processed_data/BBHI_func/sub-41064/ses-01/anat/sub-41064_ses-01_run-01_T1w.nii.gz'
t12mni_wf.inputs.input_node.MNI_ref_img = '/home/mariacabello/Downloads/average305_t1_tal_lin.nii'

#writes WF graph or runs it
t12mni_wf.write_graph()
t12mni_wf.run()
