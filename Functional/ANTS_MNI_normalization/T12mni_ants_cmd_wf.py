#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 12:37:30 2020

@author: María Cabello
"""

def get_ants_cmd_normalize_T1_MNI ():
    """Prepare Workflow to 
    Parameters
    ----------
    
    Returns
    -------
 
    """
    from os import path, environ
    from nipype import Workflow, Node
    from nipype.interfaces import utility 
    from nipype.interfaces.base import CommandLine
    from nipype.interfaces.io import DataGrabber

     #Defines workflow
    wf=Workflow(name='Normalize_Struct2MNI_cmd', base_dir='');
       
    #Setting INPUT node...
    node_input = Node(utility.IdentityInterface(fields=[
        'T1_img',
        'MNI_ref_img',
    ]),
    name='input_node')   
    
    # Reading command file (including ants-registration parameters, not including --metric)
    with open("T12mni_ants_command.txt") as file:  
        cmd = file.read()
        print(cmd)
         
    
    node_T12mni_cmd = Node(CommandLine(
        command= 'antsRegistration',
        environ={'DISPLAY': ':1'}
    ),
    name='T12mni_cmd_node')

    node_output = Node(utility.IdentityInterface(fields=[
        'struct2MNI_warp', 
        'struct2MNI_img'
    ]),
    name='output_node') 
    
    wf.connect([
#inputs         
                (node_input, node_grabber, [("T1_img", "arg2")]),
                (node_input, node_grabber, [("MNI_ref_img", "arg1")]),
#connections
                (node_grabber, node_T12mni_cmd, [("", "args")]),               
#yeld relevant data to output node
                (node_T12mni , node_output, [("composite_transform", "struct2MNI_warp")]),
                (node_T12mni, node_output,[("warped_image","struct2MNI_img")]),               
    ])
                                 
    return(wf)

