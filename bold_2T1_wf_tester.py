#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:24:43 2020

@author: root
"""
#----------------------Commands to test 


#defines WF
fmri2t1_wf=get_fmri2standard_wf([10,500])

fmri2t1_wf.base_dir=''

#sets necessary inputs
fmri2t1_wf.inputs.input_node.T1_img = 'T1.nii'
T1_img = <undefined>
func_bold_ap_img = <undefined>
func_sbref_img = <undefined>
func_segfm_ap_img = <undefined>
func_segfm_pa_img = <undefined>

#writes WF graph or runs it
fmri2t1_wf.write_graph()
fmri2t1_wf.run()