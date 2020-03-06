#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 12:37:30 2020

@author: María Cabello
"""

def get_ants_normalize_T1_MNI ():
    """Prepare Workflow to 
    Parameters
    ----------
    
    Returns
    -------
 
    """
    from os import path, environ
    from nipype import Workflow, Node
    from nipype.interfaces import ants,utility 
    
     #Defines workflow
    wf=Workflow(name='Normalize_Struct2MNI', base_dir='');
    
    
    #Setting INPUT node...
    node_input = Node(utility.IdentityInterface(fields=[
        'T1_img',
        'MNI_ref_img',
    ]),
    name='input_node')    
    
    # ¿Se dan los inputs así?
    node_T12mni = Node(ants.Registration(
        transforms=['Rigid', 'Affine', 'SyN'],
        shrink_factors=[[8,4,2,1],[8,4,2,1],[8,4,2,1]],
        smoothing_sigmas=[[3,2,1,0], [3,2,1,0], [3,2,1,0]],
        radius_or_number_of_bins=[32]*3,
        metric = ['MI']*3,
        transform_parameters=[(0.1,),(0.1,),(0.1,3,0)],
        number_of_iterations=[[1000,500,250,100],[1000,500,250,100],[1000,500,250,100]],
        write_composite_transform=True,
        metric_weight=[1]*3,
    ),
    name='T12mni_node')

    # Se recomienda usar apply
    node_output = Node(utility.IdentityInterface(fields=[
        'struct2MNI_warp', 
        'struct2MNI_img'
    ]),
    name='output_node') 
    
    wf.connect([
#inputs         
                (node_input, node_T12mni, [("T1_img", "moving_image")]),
                (node_input, node_T12mni, [("MNI_ref_img", "fixed_image")]),
#yeld relevant data to output node
                (node_T12mni , node_output, [("composite_transform", "struct2MNI_warp")]),
                (node_T12mni, node_output,[("warped_image","struct2MNI_img")]),               
    ])
                                 
    return(wf)

