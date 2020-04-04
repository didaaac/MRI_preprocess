# 13/02/2020 María Cabello
# This bash script transform the glasser atlas from fsaverage (surface) to native BoldStandard volume of each subject in SUBJECTS_DIR

#**************** USAGE ******************
#run_all_glasser_surf2vol_native_BOLD.sh --subjects_dir <reconall_folder> --subject_id <sub-XXXXX> --left_annotation <path_to_left_annotfile> --right_annotation <path_to_right_annotfile> --output_dir <output_folder>
#bash <where_this_script_is>/run_all_glasser_surf2vol_native_BOLD.sh --subjects_dir /home/mariacabello/wf_workspace/thesis_data/recon_all --left_annotation fsaverage/lh.HCP-MMP1.annot --right_annotation fsaverage/rh.HCP-MMP1.annot --output_dir /home/mariacabello/wf_workspace/thesis_data/glasser
#***************************************** 

#Values assigned by default if not given as arguments

OUTPUT_FOLDER='/home/mariacabello/wf_workspace/thesis_data/glasser' # /{subj}/
SUBJECTS_DIR='/home/mariacabello/wf_workspace/thesis_data/recon_all'
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


list_subs=$(ls $SUBJECTS_DIR/* -d)
separate="##################################################################################"

done_subs=$(ls $OUTPUT_FOLDER/* -d)

done_subs_list=""
for done_sub in $done_subs; do
	done_subs_list="$done_subs_list $(basename $done_sub)"
done


for i in $list_subs; do
	SUBJECT_ID=$(basename $i)
	if [[ $SUBJECT_ID == *"sub"* ]]; then #to avoid folders that are not for a subject, e.g. /fsaverage
		if [[ $done_subs_list =~ (^|[[:space:]])$SUBJECT_ID($|[[:space:]]) ]]; then
			echo $separate
			echo "Glasser atlas already obtained for $SUBJECT_ID"
			#bash /home/mariacabello/git_projects/MRI_preprocess/Structural/glasser2016/glasser_surf2vol_native_BOLD.sh --subjects_dir $SUBJECTS_DIR --subject_id $SUBJECT_ID --left_annotation $GLASSER_FSAVERAGE_LEFT --right_annotation $GLASSER_FSAVERAGE_RIGHT --output_dir $OUTPUT_FOLDER
			bash /home/mariacabello/git_projects/MRI_preprocess/Structural/glasser374/subcortical14.sh --subjects_dir $SUBJECTS_DIR --subject_id $SUBJECT_ID --output_dir $OUTPUT_FOLDER
		else 
			echo "Obtaining Glasser Atlas for $SUBJECT_ID"
			#bash /home/mariacabello/git_projects/MRI_preprocess/Structural/glasser2016/glasser_surf2vol_native_BOLD.sh --subjects_dir $SUBJECTS_DIR --subject_id $SUBJECT_ID --left_annotation $GLASSER_FSAVERAGE_LEFT --right_annotation $GLASSER_FSAVERAGE_RIGHT --output_dir $OUTPUT_FOLDER
			#bash /home/mariacabello/git_projects/MRI_preprocess/Structural/glasser374/subcortical14.sh --subjects_dir $SUBJECTS_DIR --subject_id $SUBJECT_ID --output_dir $OUTPUT_FOLDER
		fi
	fi

done
