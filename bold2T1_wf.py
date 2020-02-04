#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:27:39 2020
@author: Dídac Macià
"""


def get_fmri2standard_wf(tvols, ACQ_PARAMS):
    """Prepare Workflow to 
    
    1)realign BOLD
    2)corregister SB_ref + MB_bold to SE_gfm_AP 
    3)estimate unwarping with TOPUP
    4)apply topup to SB_ref and MB_bold
    5)corregister SB_ref to T1_anat and apply it to MB_bold 

    Parameters
    ----------
    

    Returns
    -------
 
    """
    from os import path
    from nipype.algorithms import confounds
    #from nipype.interfaces.utility import Function
    from nipype import Workflow, Node, MapNode, Function, interfaces
    from nipype.interfaces import fsl, utility 
      
    print("defining workflow...");
    wf=Workflow(name='fmri2standard', base_dir='');
    
    #Setting INPUT node...
    node_input = Node(utility.IdentityInterface(fields=[
        'func_sbref_img', 
        'func_segfm_ap_img',
        'func_segfm_pa_img',
        'func_bold_ap_img',
        'T1_img'
    ]),
    name='input_node') 
    
    
    
    print ("Preparing corregister of SBref to SEgfm space...");
    node_average_SEgfm = Node(fsl.maths.MeanImage(
           # in_file=SUBJECT_FSTRUCT_DIC['func_se_gfm_ap']                                     
            ),
    name='Mean_SEgfm_AP'
    );  
    node_coregister_SBref2SEgfm=Node(fsl.FLIRT(
                        # in_file=SUBJECT_FSTRUCT_DIC['func_sb_ref'],
                         dof=6
                         ),
    name='Corregister_SBref2SEgfm'
    );   
    
    
    
    print ("Preparing McFLirt with SB EPI reference...");
    
    node_eliminate_first_scans=Node(fsl.ExtractROI(
            t_min=tvols[0],
            t_size=tvols[1]- tvols[0],
           # in_file=SUBJECT_FSTRUCT_DIC['func_bold'],
           # ref_file=SUBJECT_FSTRUCT_DIC['func_sb_ref'],
           
            ),
    name="eliminate_first_scans"
    );
    
    node_realign_bold=Node(fsl.MCFLIRT(
           # in_file=SUBJECT_FSTRUCT_DIC['func_bold'],
           # ref_file=SUBJECT_FSTRUCT_DIC['func_sb_ref'],
            save_plots=True,
            ),
    name="realign_fmri2SBref"
    );
      
    print("Preparing TSNR image for QA...")
    node_tsnr =Node(confounds.TSNR(
            regress_poly=2
            ),
    name="QA_TSNR"
    );
    
 
    print ("Preparing AP-PA TOPUP estimation...");
    node_merge_ap_pa_inputs = Node(utility.base.Merge(2),name='Merge_ap_pa_inputs')
    
    node_merge_SEgfm=Node(fsl.Merge(
           # in_files = [SUBJECT_FSTRUCT_DIC['func_se_gfm_ap'],
           #             SUBJECT_FSTRUCT_DIC['func_se_gfm_pa']],
            dimension = 't'   
            ),
    name='Merge_SEgfm_AP_PA'
    );
    
    '''
    write_acqparams_file_interface = Function(input_names=["out_file", "scan_value"],
                             output_names=["acqparams_file"],
                             function=write_acqparams_file);
    write_acqparams_file_interface.inputs.out_file=path.join(wf.base_dir,'acparams_hcp.txt');
    node_write_acpparams_file=Node(interface=write_acqparams_file_interface,
                                   name='Write_acqparam_file'
    );
    '''
    
    node_topup_SEgfm=Node(fsl.TOPUP(#in_file=OUT_FOLDER + os.sep+ 'sefm_ap_pa.nii.gz', 
                  encoding_file=ACQ_PARAMS,
                    ),
    name='Topup_SEgfm_estimation'
    );
    
    print ("Preparing TOPUP applywarp...");
    node_apply_topup= Node(fsl.ApplyTOPUP(
                            encoding_file=ACQ_PARAMS,
                            #in_index=[1],
                            #in_topup_movpar=OUT_FOLDER + os.sep+'topup_movpar.txt',
                            #in_topup_fieldcoef=OUT_FOLDER + os.sep+ 'topup_fieldcoef.nii.gz',
                            method='jac',
                            interp='spline',
                            #out_corrected=OUT_FOLDER + os.sep+'unwarped_sb_ref.nii.gz' 
                            ), 
    name="apply_topup");
           
                                   
    #Registration to T1. Epireg without fieldmaps combined (see https://www.fmrib.ox.ac.uk/primers/intro_primer/ExBox20/IntroBox20.html)                    

    print ("Corregister BOLD to T1...");
    node_mask_T1=Node(fsl.BET(
           # in_file=SUBJECT_FSTRUCT_DIC['anat_T1'],
            frac=0.7
            ),
    name="mask_T1");   

    node_epireg = Node(fsl.EpiReg(
            #t1_head=SUBJECT_FSTRUCT_DIC['anat_T1'],
            out_base='SEgfm2T1'
            ),
    name="epi2reg");
                      
    print ("Getting mask for fMRI space...");
    node_invert_epi2reg= Node(fsl.ConvertXFM(
            invert_xfm=True),
    name="invert_epi2reg");
                                                                    
        
    node_fmriMask=Node(fsl.BET(mask=True,),
    name='fmriMask'
    );   
    #node_fmriMask.overwrite=True
    print ("Setting OUTPUT node...");
    node_output = Node(interfaces.utility.IdentityInterface(fields=[
        'SBref2SEgfm_mat', 
        'realign_movpar_txt',
        'realign_fmri_img',
        'topup_movpar_txt',
        'topup_field_coef_img',
        'epi2str_mat',
        'fmri_mask_img',
        'rfmri_unwarped_imgs',
        'sb_ref_unwarped_img',
    ]),
    name='output_node')  
                                                     
    #Connects nodes
    wf.connect([
#inputs         
                (node_input, node_average_SEgfm, [("func_segfm_ap_img", "in_file")]),
                (node_input, node_coregister_SBref2SEgfm, [("func_sbref_img", "in_file")]),
                (node_input, node_eliminate_first_scans, [("func_bold_ap_img", "in_file")]),
                (node_input, node_merge_ap_pa_inputs,[("func_segfm_ap_img", "in1"),
                                                      ("func_segfm_pa_img", "in2")
                ]),
                (node_merge_ap_pa_inputs, node_merge_SEgfm,[("out", "in_files")]),
                (node_input, node_epireg, [("T1_img", "t1_head")]),
                (node_input, node_mask_T1, [("T1_img", "in_file")]),
                                            
#connections    
                (node_eliminate_first_scans, node_realign_bold, [("roi_file", "in_file")]),
                (node_average_SEgfm , node_coregister_SBref2SEgfm, [("out_file", "reference")]),
                (node_coregister_SBref2SEgfm , node_realign_bold, [("out_file", "ref_file")]),
                
                #(node_realign_bold, node_tsnr, [("out_file", "in_file")]),                 
                (node_merge_SEgfm, node_topup_SEgfm, [("merged_file", "in_file")]),              
                (node_realign_bold , node_apply_topup, [("out_file", "in_files")]),
                (node_topup_SEgfm , node_apply_topup, [("out_fieldcoef", "in_topup_fieldcoef"),
                                                       ("out_movpar","in_topup_movpar") ]),
#corregister to T1
                (node_mask_T1 , node_epireg, [("out_file", "t1_brain")]),
                (node_topup_SEgfm , node_epireg, [("out_corrected", "epi")]),
                (node_epireg,node_invert_epi2reg,[("epi2str_mat", "in_file")]),
                (node_coregister_SBref2SEgfm,node_fmriMask,[("out_file", "in_file")]),
#yeld relevant data to output node
                (node_coregister_SBref2SEgfm , node_output, [("out_matrix_file", "SBref2SEgfm_mat")]),
                (node_realign_bold , node_output, [("par_file", "realign_movpar_txt"),
                                                   ("out_file","realign_fmri_img")]),
                (node_fmriMask , node_output, [("mask_file", "fmri_mask_img")]),
                (node_epireg, node_output, [("epi2str_mat", "epi2str_mat")]), 
                (node_topup_SEgfm, node_output, [("out_fieldcoef", "topup_field_coef_img"),
                                                 ("out_corrected","sb_ref_unwarped_img")]),
                (node_apply_topup, node_output,[("out_corrected","rfmri_unwarped_imgs")]),
                
    ]);      
    return(wf);