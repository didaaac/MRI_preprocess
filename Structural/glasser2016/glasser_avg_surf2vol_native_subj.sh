# 13/02/2020 María Cabello
# This bash script transform the glasser atlas from fsaverage (surface) to native structural volume of each subject in SUBJECTS_DIR

# !!!! OUTPUT FOLDER TO BE CHANGED; from mariacabello user to NASS
OUTPUT_FOLDER='/home/mariacabello/wf_workspace/glasser_surf2vol' # /{subj}/

SUBJECTS_DIR='/institut/processed_data/BBHI_output/structural'

#Taking into account that in the same folder this scrpit is, there is a folder 'fsaverage' containing glasser annotations
GLASSER_FSAVERAGE_LEFT='fsaverage/lh.HCP-MMP1.annot'
GLASSER_FSAVERAGE_RIGHT='fsaverage/rh.HCP-MMP1.annot'


list_subs=$(ls $SUBJECTS_DIR/* -d)
separate="##################################################################################"

for i in $list_subs; do
	SUBJECT_ID=$(basename $i)
	if [[ $SUBJECT_ID == *"sub"* ]]; then #to avoid folders that are not for a subject, e.g. /fsaverage
		
		#create folders if not exist
		mkdir -p /$OUTPUT_FOLDER/$SUBJECT_ID

		echo $separate
		echo $separate		
		echo "Processing subject $SUBJECT_ID..."
		echo $separate	
		echo "... from fsaverage to native (surf2surf) -- LEFT"
		mri_surf2surf --srcsubject fsaverage --sval-annot $GLASSER_FSAVERAGE_LEFT --trgsubject $SUBJECT_ID --tval $OUTPUT_FOLDER/$SUBJECT_ID/lh.HCP-MMP1.annot --hemi lh
		echo $separate	
		echo "... from fsaverage to native (surf2surf) -- RIGHT"
		mri_surf2surf --srcsubject fsaverage --sval-annot $GLASSER_FSAVERAGE_RIGHT --trgsubject $SUBJECT_ID --tval $OUTPUT_FOLDER/$SUBJECT_ID/rh.HCP-MMP1.annot --hemi rh

		echo $separate	
		echo "... from native surface to native volumetric (T1) (label2vol) -- LEFT"
		mri_label2vol --annot $OUTPUT_FOLDER/$SUBJECT_ID/lh.HCP-MMP1.annot --temp $SUBJECTS_DIR/$SUBJECT_ID/mri/T1.mgz --identity --fillthresh .3 --proj frac 0 1 .1  --subject $SUBJECT_ID --o $OUTPUT_FOLDER/$SUBJECT_ID/glasser_volumetric_T1_lh.nii.gz --hemi lh
		echo $separate	
		echo "... from native surface to native volumetric (T1) (label2vol) -- RIGHT"
		mri_label2vol --annot $OUTPUT_FOLDER/$SUBJECT_ID/rh.HCP-MMP1.annot --temp $SUBJECTS_DIR/$SUBJECT_ID/mri/T1.mgz --identity --fillthresh .3 --proj frac 0 1 .1  --subject $SUBJECT_ID --o $OUTPUT_FOLDER/$SUBJECT_ID/glasser_volumetric_T1_rh.nii.gz --hemi rh
	fi
done

