#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 19:06:16 2020

@author: mariacabello
"""

import nibabel as nib
import numpy as np

class Glasser:
    '''
    '''
    def __init__(self,
                 left_annot_path="/home/mariacabello/git_projects/MRI_preprocess/Structural/glasser2016/fsaverage/lh.HCP-MMP1.annot", 
                 right_annot_path="/home/mariacabello/git_projects/MRI_preprocess/Structural/glasser2016/fsaverage/rh.HCP-MMP1.annot",
                 masks_root_path="/home/mariacabello/wf_workspace/thesis_data/glasser",
                 left_mask_filename="glasser_volumetric_T1_lh_boldT1.nii.gz",
                 right_mask_filename="glasser_volumetric_T1_rh_boldT1.nii.gz",
                 total_mask_filename="glasser_volumetric_T1_boldT1.nii.gz"):
       self.left_annot = nib.freesurfer.io.read_annot(left_annot_path)
       self.right_annot = nib.freesurfer.io.read_annot(right_annot_path)
       self.annot_labels = [list([i, self.left_annot[2][i].decode('ascii')]) if i<len(self.left_annot[2]) else list([i, self.right_annot[2][i-(len(self.left_annot[2])-1)].decode('ascii')])for i in range(len(self.left_annot[2])*2-1) ]
       
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
       self.total_mask_filename=total_mask_filename
       

    def get_annot_labels(self, annot):
        return [list([i, annot[2][i].decode('ascii')]) for i in range(len(annot[2]))]


    def write_total_mask(self, subject_id):
        '''
        '''
        left_mask = nib.load(self.masks_root_path+'/'+subject_id+'/'+self.left_mask_filename).get_data()
        right_mask = nib.load(self.masks_root_path+'/'+subject_id+'/'+self.right_mask_filename).get_data()
        affine = nib.load(self.masks_root_path+'/'+subject_id+'/'+self.right_mask_filename).affine
        
        simult_coords = np.where(np.logical_and(left_mask>0, right_mask>0))
        
        right_mask = right_mask + 180
        right_mask[right_mask==180]=0
        complete_mask = left_mask + right_mask
        
        complete_mask[simult_coords] = 0 #THIS iS NOT OK

        complete = nib.Nifti1Image(complete_mask, affine)
        complete.to_filename(self.masks_root_path+'/'+subject_id+'/'+self.total_mask_filename)
        
        return complete_mask

    def extract_timeseries(self, subject_id, bold_file_path, output_file):
        '''
        '''
        import os.path
        
        print("################")
        print(subject_id)
        print("################")
              
        print("Reading bold...")
        bold_img = nib.load(bold_file_path).get_data()
        print("Bold readed")

        if os.path.isfile(self.masks_root_path+'/'+subject_id+'/'+self.total_mask_filename):
            print("Complete mask (left+right) already exist. Reading...")
        else:
            print("Complete mask (left+right) does not exist. Writing...")
            self.write_total_mask(subject_id=subject_id)
            print("Complete mask (left+right) created! Reading...")
            
        mask = nib.load(self.masks_root_path+'/'+subject_id+'/'+self.total_mask_filename).get_data()
        
        print("Complete mask readed")
        
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
        np.savetxt(output_file, timeseries)
        print("Timeseries saved")
        
