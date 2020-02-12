#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#use of the script
#source activate python2_7
#heudiconv -d /institut/BBHI_DICOMS/{subject}/*/*IMA -s 162766 -ss 01 -f /home/didac/Scripts/dicom2BIDS/convert_BBHI.py  -c dcm2niix -b -o /institut/processed_data/BBHI_func 



import os

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    t1w=create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:02d}_T1w')
    t2w=create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:02d}_T2w')
    flair=create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:02d}_FLAIR')
    swi_mag=create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:02d}_swi_mag')  
    swi_phase=create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:02d}_swi_phase') 
    swi_mIP=create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:02d}_swi_mIP') 
    swi_comb=create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:02d}_swi_comb') 
    
    rest_bold_ap=create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_run-{item:02d}_rest_bold_ap') 
    rest_bold_pa=create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_run-{item:02d}_rest_bold_pa') 
    rest_sbref_ap=create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_run-{item:02d}_rest_sbref_ap')
    rest_sbref_pa=create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_run-{item:02d}_rest_sbref_pa')
    rest_sefm_ap=create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_run-{item:02d}_rest_sefm_ap')
    rest_sefm_pa=create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_run-{item:02d}_rest_sefm_pa') 

    dwi_dir_ap=create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_run-{item:02d}_dwi_dir_ap-') 
    dwi_dir_pa=create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_run-{item:02d}_dwi_dir_pa') 
    dwi_sefm_ap=create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_run-{item:02d}_dwi_sefm_ap') 
    dwi_sefm_pa=create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_run-{item:02d}_dwi_sefm_pa') 
    
    pcasl_epi_ap=create_key('sub-{subject}/{session}/perf/sub-{subject}_{session}_run-{item:02d}_perf_vol_ap') 
    pcasl_epi_pa=create_key('sub-{subject}/{session}/perf/sub-{subject}_{session}_run-{item:02d}_perf_vol_pa') 
    pcasl_sefm_ap=create_key('sub-{subject}/{session}/perf/sub-{subject}_{session}_run-{item:02d}_perf_sefm_ap') 
    pcasl_sefm_pa=create_key('sub-{subject}/{session}/perf/sub-{subject}_{session}_run-{item:02d}_perf_sefm_pa') 
       
    info =  {
                    t1w:[],
                    t2w:[],
                    flair:[],
                    swi_mag:[],
                    swi_phase:[],
                    swi_mIP:[],
                    swi_comb:[],
                    rest_bold_ap:[],
                    rest_bold_pa:[],
                    rest_sbref_ap:[],
                    rest_sbref_pa:[],
                    rest_sefm_pa:[],
                    rest_sefm_ap:[],
                    dwi_dir_ap:[],
                    dwi_dir_pa:[],
                    dwi_sefm_ap:[],
                    dwi_sefm_pa:[],
                    pcasl_epi_ap:[],
                    pcasl_epi_pa:[],
                    pcasl_sefm_ap:[],
                    pcasl_sefm_pa:[],
             }
    for s in seqinfo:
        #print('-------------------------------------------------')
        #print(acq)
        #print('-------------------------------------------------')
        if s.protocol_name=='T1w_MPR':
            info[t1w].append(s.series_id)   
        if s.protocol_name=='T2w_SPC':
            info[t2w].append(s.series_id) 
        if s.protocol_name=='FLAIR':
            info[flair].append(s.series_id)          
        #swi
        if s.protocol_name=='SWI':
            if s.image_type[2]=='P':
                info[swi_phase].append(s.series_id)  
            elif s.image_type[2]=='MNIP':
                info[swi_mIP].append(s.series_id)
            elif s.image_type[3]=='SWI':
                info[swi_comb].append(s.series_id)
            else :
                info[swi_mag].append(s.series_id)
                
        #pCASL
        if s.protocol_name=='pCASL_AP': 
            if s.sequence_name=='epse2d1_86':
                info[pcasl_sefm_ap].append(s.series_id)
            elif s.sequence_name=='mbPCASL2d1_86':
                info[pcasl_epi_ap].append(s.series_id)
        if s.protocol_name=='pCASL_PA': 
            if s.sequence_name=='epse2d1_86':
                info[pcasl_sefm_pa].append(s.series_id)
            elif s.sequence_name=='mbPCASL2d1_86':
                info[pcasl_epi_pa].append(s.series_id)
            
            
        """
        The namedtuple `s` contains the following fields:

        * total_files_till_now
        * example_dcm_file
        * series_id
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * image_type
        """
    
    
    return info