# 13/02/2020 María Cabello
# This bash script transforms the glasser atlas from fsaverage (surface) to native BoldStandard volume of each subject in SUBJECTS_DIR 
# and adds 14 subcortical regions

#**************** USAGE ******************
#subcortical14.sh --subjects_dir <> --ourput_dir <>
#bash <where_this_script_is>/subcrotical14.sh 
#***************************************** 

OUTPUT_FOLDER='/home/mariacabello/wf_workspace/thesis_data/glasser' # /{subj}/
SUBJECTS_DIR='/home/mariacabello/wf_workspace/thesis_data/recon_all'
SUBJECT_ID='sub-103151'

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    --subject_dir)
    SUBJECT_DIR="$2"
    shift # past argument
    shift # past value
    ;;
    --subject_id)
    SUBJECT_ID="$2"
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

ASEG_FILE=$SUBJECTS_DIR/$SUBJECT_ID/mri/aseg.mgz
REFERENCE_FILE=/home/mariacabello/wf_workspace/thesis_data/fmri2standard/$SUBJECT_ID/spm_coregister2T1_sbref/${SUBJECT_ID}_ses-01_run-01_rest_sbref_ap_flirt_corrected_coregistered2T1.nii.gz
OUTPUT_FOLDER=$OUTPUT_FOLDER/$SUBJECT_ID

#LEFT

#17 L_Hippocampus -> 1
#18 L_Amygdala -> 2
#13 L_Pallidum -> 3
#12 L_Putamen -> 4
#11 L_Caudate -> 5
#26 L_Accumbens -> 6
#10 L_Thalamus -> 7

left_subcortical_labels="17 18 13 12 11 26 10"

i=1
for lab in $left_subcortical_labels; do
	mri_binarize --i $ASEG_FILE --match $lab --o $OUTPUT_FOLDER/tmp.mgz
	echo "1"
	mri_vol2vol --mov $OUTPUT_FOLDER/tmp.mgz --regheader --targ $REFERENCE_FILE --o $OUTPUT_FOLDER/tmp_sbref.mgz --interp nearest
	echo "2"
	mri_convert --in_type mgz --out_type nii $OUTPUT_FOLDER/tmp_sbref.mgz $OUTPUT_FOLDER/tmp.nii.gz
	echo "3"
	#fslmaths $OUTPUT_FOLDER/tmp.nii.gz -bin $OUTPUT_FOLDER/tmp_binmask.nii.gz
	echo "4"
	if [ $lab -eq ${left_subcortical_labels%% *} ]; then
		fslmaths $OUTPUT_FOLDER/tmp.nii.gz -mul $i $OUTPUT_FOLDER/left_subcortical14.nii.gz
		echo "5"
	else
		fslmaths $OUTPUT_FOLDER/tmp.nii.gz -mul $i $OUTPUT_FOLDER/tmp.nii.gz
		echo "5"
		fslmaths $OUTPUT_FOLDER/left_subcortical14.nii.gz -add $OUTPUT_FOLDER/tmp.nii.gz $OUTPUT_FOLDER/left_subcortical14.nii.gz
		echo "6"
	fi
	i=$((i+1))
done

#RIGTH

#53 R_Hippocampus -> 1
#54 R_Amygdala -> 2
#52 R_Pallidum -> 3
#51 R_Putamen -> 4
#50 R_Caudate -> 5
#58 R_Accumbens -> 6
#49 R_Thalamus -> 7

right_subcortical_labels="53 54 52 51 50 58 49"

i=1
for lab in $right_subcortical_labels; do
	mri_binarize --i $ASEG_FILE --match $lab --o $OUTPUT_FOLDER/tmp.mgz
	echo "1"
	mri_vol2vol --mov $OUTPUT_FOLDER/tmp.mgz --regheader --targ $REFERENCE_FILE --o $OUTPUT_FOLDER/tmp_sbref.mgz --interp nearest
	echo "2"
	mri_convert --in_type mgz --out_type nii $OUTPUT_FOLDER/tmp_sbref.mgz $OUTPUT_FOLDER/tmp.nii.gz
	echo "3"
	#fslmaths $OUTPUT_FOLDER/tmp.nii.gz -bin $OUTPUT_FOLDER/tmp_binmask.nii.gz
	echo "4"
	if [ $lab -eq ${right_subcortical_labels%% *} ]; then
		fslmaths $OUTPUT_FOLDER/tmp.nii.gz -mul $i $OUTPUT_FOLDER/right_subcortical14.nii.gz
		echo "5"
	else
		fslmaths $OUTPUT_FOLDER/tmp.nii.gz -mul $i $OUTPUT_FOLDER/tmp.nii.gz
		echo "5"
		fslmaths $OUTPUT_FOLDER/right_subcortical14.nii.gz -add $OUTPUT_FOLDER/tmp.nii.gz $OUTPUT_FOLDER/right_subcortical14.nii.gz
		echo "6"
	fi
	i=$((i+1))
done

#rm $OUTPUT_FOLDER/tmp_binmask.nii.gz
rm $OUTPUT_FOLDER/tmp.nii.gz
rm $OUTPUT_FOLDER/tmp.mgz
rm $OUTPUT_FOLDER/tmp_sbref.mgz
