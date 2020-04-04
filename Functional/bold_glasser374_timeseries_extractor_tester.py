#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:16:34 2020

@author: mariacabello
"""

from bold_glasser374_timeseries_extractor import Glasser374

glasser = Glasser374()

list_subjs = [#"sub-103151",
#              "sub-116245",
#              "sub-129073",
#              "sub-151965",
              
              "sub-187232",
              "sub-50000",
              "sub-86143",
              "sub-92918",

              "sub-161022",
              "sub-48296",
              "sub-73417",
              "sub-88604",
              "sub-93338",

              "sub-185225",
              "sub-49664",
              "sub-84766",
              "sub-92889"        
        ]

for subj in list_subjs:
    output_file="/home/mariacabello/wf_workspace/thesis_data/timeseries/glasser374/{subject_id}_timeseries_glasser374.txt".format(subject_id=subj)
    bold_img_filename="/home/mariacabello/wf_workspace/thesis_data/nuisance_correction/{subject_id}/filter_regressors_bold/{subject_id}_ses-01_run-01_rest_bold_ap_roi_mcf_corrected_coregistered2T1_regfilt.nii.gz".format(subject_id=subj)
    glasser.extract_374timeseries(subj, bold_img_filename, output_file)
