#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 19:06:16 2020

@author: mariacabello
"""

import nibabel as nib
import numpy as np


class Glasser374:
    '''
    '''
    def __init__(self,
                 left_annot_path="/home/mariacabello/git_projects/MRI_preprocess/Structural/glasser2016/fsaverage/lh.HCP-MMP1.annot", 
                 right_annot_path="/home/mariacabello/git_projects/MRI_preprocess/Structural/glasser2016/fsaverage/rh.HCP-MMP1.annot",
                 masks_root_path="/home/mariacabello/wf_workspace/thesis_data/glasser",
                 left_mask_filename="glasser_volumetric_T1_lh_boldT1.nii.gz",
                 right_mask_filename="glasser_volumetric_T1_rh_boldT1.nii.gz",
                 left_submask_annot_path="/home/mariacabello/git_projects/MRI_preprocess/Structural/glasser374/left_subcortical_aseg_labels.txt",
                 right_submask_annot_path="/home/mariacabello/git_projects/MRI_preprocess/Structural/glasser374/right_subcortical_aseg_labels.txt",
                 left_submask_filename="left_subcortical14.nii.gz",
                 right_submask_filename="right_subcortical14.nii.gz"):
       self.left_annot = nib.freesurfer.io.read_annot(left_annot_path)
       self.right_annot = nib.freesurfer.io.read_annot(right_annot_path)
       self.annot_labels = [list([i, self.left_annot[2][i].decode('ascii')]) if i<len(self.left_annot[2]) else list([i, self.right_annot[2][i-(len(self.left_annot[2])-1)].decode('ascii')])for i in range(len(self.left_annot[2])*2-1) ]
       self.right_submask_filename=right_submask_filename
       self.left_submask_filename=left_submask_filename
       
       #MAL
#       real_labels = [j if j <len(left_annot[2]) else j-len(left_annot[2])+1 for j in range(len(left_annot[2])*2-1)]
#       self.annot_labels = np.vstack((np.array([real_labels,]), np.array(annot_labels).transpose())).transpose()
#       left_submask_annot_labels = np.genfromtxt(left_submask_annot_path, delimiter=' ', dtype=str)
#       right_submask_annot_labels = np.genfromtxt(right_submask_annot_path, delimiter=' ', dtype=str)
#       a = []
       
       
#       [list([i, left_annot[2][i].decode('ascii')]) if i<len(left_annot[2]) else list([i, right_annot[2][i-len(left_annot[2])].decode('ascii')]) for i in range(len(left_annot[2])*2-1)]
#       for i in range(len(left_annot[2])*2-1):
#           if i<len(left_annot[2]):
#               print(list([i, left_annot[2][i].decode('ascii')]))
#           else:
#               print(i-(len(left_annot[2])-1))
#               print(list([i, right_annot[2][i-(len(left_annot[2])-1)].decode('ascii')]))
       
       self.masks_root_path=masks_root_path
       self.left_mask_filename=left_mask_filename
       self.right_mask_filename=right_mask_filename
       

    def get_annot_labels(self, annot):
        return [list([i, annot[2][i].decode('ascii')]) for i in range(len(annot[2]))]

#WRONG
#    def write_total_mask(self, subject_id):
#        '''
#        '''
#        left_mask = nib.load(self.masks_root_path+'/'+subject_id+'/'+self.left_mask_filename).get_data()
#        right_mask = nib.load(self.masks_root_path+'/'+subject_id+'/'+self.right_mask_filename).get_data()
#        affine = nib.load(self.masks_root_path+'/'+subject_id+'/'+self.right_mask_filename).affine
#        
#        simult_coords = np.where(np.logical_and(left_mask>0, right_mask>0))
#        
#        right_mask = right_mask + 180
#        right_mask[right_mask==180]=0
#        complete_mask = left_mask + right_mask
#        
#        complete_mask[simult_coords] = 0
#
#        complete = nib.Nifti1Image(complete_mask, affine)
#        complete.to_filename(self.masks_root_path+'/'+subject_id+'/'+self.total_mask_filename)
#        
#        return complete_mask

    def extract_374timeseries(self, subject_id, bold_file_path, output_file):
        '''
        '''
        import os.path
        
        print("################")
        print(subject_id)
        print("################")
              
        print("Reading bold...")
        bold_img = nib.load(bold_file_path).get_data()
        print("Bold readed")

        #GLASSER 360
        print("Reading and extracting timeseries (left glasser360 mask)...")
        left_mask = nib.load(self.masks_root_path+'/'+subject_id+'/'+self.left_mask_filename).get_data()
        left_timeseries = self.extract_timeseries(left_mask, bold_img)
        print("Left glasser360 done!")
        
        print("Reading and extracting timeseries (right glasser360 mask)...")
        right_mask = nib.load(self.masks_root_path+'/'+subject_id+'/'+self.right_mask_filename).get_data()
        right_timeseries = self.extract_timeseries(right_mask, bold_img)
        print("Right glasser360 done!")
        
        #SUBCORTICAL14
        print("Reading left subcortical14 mask...")
        left_sub_mask = nib.load(self.masks_root_path+'/'+subject_id+'/'+self.left_submask_filename).get_data()
        left_sub_timeseries = self.extract_timeseries(left_sub_mask, bold_img)
        print("Left subcortical14 done!")
        
        print("Reading right subcortical14 mask...")
        right_sub_mask = nib.load(self.masks_root_path+'/'+subject_id+'/'+self.right_submask_filename).get_data()
        right_sub_timeseries = self.extract_timeseries(right_sub_mask, bold_img)
        print("Right subcortical14 done!")
        
        timeseries = np.vstack((left_timeseries, right_timeseries, left_sub_timeseries, right_sub_timeseries))
        
        np.savetxt(output_file, timeseries)
        print("Timeseries saved")
        
    
    def extract_timeseries(self, mask, bold_img):
        print("Extracting timeseries (from 1 to " + str(mask.max()) + ")")
        for i in range(int(1),int(mask.max()+1)):
            ROI_timeseries = []
            coords = np.where(mask==i)
            for t in range(0,bold_img.shape[3]):
                ROI_timeseries.append(np.mean(bold_img[coords[0], coords[1], coords[2], t]))
            if i==1:
                timeseries = ROI_timeseries
            else:
                timeseries = np.vstack((timeseries, ROI_timeseries))
        print("Timeseries extracted!")
        return timeseries
