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
    wf=Workflow(name='Normalize_Struct2MNI');
    
    
    #Setting INPUT node...
    node_input = Node(utility.IdentityInterface(fields=[
        'T1_img', 
        'MNI_ref_img',
    ]),
    name='input_node')    

    node_output = Node(utility.IdentityInterface(fields=[
        'struct2MNI_warp', 
        'struct2MNI_img'
    ]),
    name='output_node') 
                                 
    return(wf)
