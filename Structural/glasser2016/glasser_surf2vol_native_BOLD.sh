# 13/02/2020 María Cabello
# This bash script transform the glasser atlas from fsaverage (surface) to native BoldStandard volume of a given subject in SUBJECTS_DIR

#**************** USAGE ******************
#glasser_surf2vol_native_BOLD.sh --subjects_dir <reconall_folder> --subject_id <sub-XXXXX> --left_annotation <path_to_left_annotfile> --right_annotation <path_to_right_annotfile> --output_dir <output_folder>
#bash <where_this_script_is>/glasser_surf2vol_native_BOLD.sh --subjects_dir /home/mariacabello/wf_workspace/thesis_data/recon_all --subject_id sub-103151 --left_annotation <path_to_left_annotfile> --right_annotation <path_to_right_annotfile> --output_dir /home/mariacabello/wf_workspace/thesis_data/glasser
#***************************************** 

#Values assigned by default if not given as arguments

OUTPUT_FOLDER='/home/mariacabello/wf_workspace/thesis_data/glasser' # /{subj}/
SUBJECTS_DIR='/home/mariacabello/wf_workspace/thesis_data/recon_all'
SUBJECT_ID='sub-103151'
#Taking into account that in the same folder this scrpit is, there is a folder 'fsaverage' containing glasser annotations
GLASSER_FSAVERAGE_LEFT='fsaverage/lh.HCP-MMP1.annot'
GLASSER_FSAVERAGE_RIGHT='fsaverage/rh.HCP-MMP1.annot'

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    --subjects_dir)
    SUBJECTS_DIR="$2"
    shift # past argument
    shift # past value
    ;;
    --subject_id)
    SUBJECT_ID="$2"
    shift # past argument
    shift # past value
    ;;
    --left_annotation)
    GLASSER_FSAVERAGE_LEFT="$2"
    shift # past argument
    shift # past value
    ;;
    --right_annotation)
    GLASSER_FSAVERAGE_RIGHT="$2"
    shift # past argument
    shift # past value
    ;;
    --output_dir)
    OUTPUT_FOLDER="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done


SBREF_T1=/home/mariacabello/wf_workspace/thesis_data/fmri2standard/$SUBJECT_ID/spm_coregister2T1_sbref/${SUBJECT_ID}_ses-01_run-01_rest_sbref_ap_flirt_corrected_coregistered2T1.nii.gz
BOLD_T1=/home/mariacabello/wf_workspace/thesis_data/fmri2standard/$SUBJECT_ID/spm_coregister2T1_bold/${SUBJECT_ID}_ses-01_run-01_rest_bold_ap_roi_mcf_corrected_coregistered2T1.nii.gz

#create folders if not exist
mkdir -p $OUTPUT_FOLDER/$SUBJECT_ID

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
mri_vol2vol --mov $OUTPUT_FOLDER/$SUBJECT_ID/glasser_volumetric_T1_lh.nii.gz --targ $SBREF_T1 --o $OUTPUT_FOLDER/$SUBJECT_ID/glasser_volumetric_T1_lh_boldT1.nii.gz --regheader --interp nearest

echo $separate
echo "... from native surface to native volumetric (T1) (label2vol) -- RIGHT"
mri_label2vol --annot $OUTPUT_FOLDER/$SUBJECT_ID/rh.HCP-MMP1.annot --temp $SUBJECTS_DIR/$SUBJECT_ID/mri/T1.mgz --identity --fillthresh .3 --proj frac 0 1 .1  --subject $SUBJECT_ID --o $OUTPUT_FOLDER/$SUBJECT_ID/glasser_volumetric_T1_rh.nii.gz --hemi rh
echo $separate
mri_vol2vol --mov $OUTPUT_FOLDER/$SUBJECT_ID/glasser_volumetric_T1_rh.nii.gz --targ $SBREF_T1 --o $OUTPUT_FOLDER/$SUBJECT_ID/glasser_volumetric_T1_rh_boldT1.nii.gz --regheader --interp nearest




