#BATCH for freesurfer -- bash
#Enter subject_dir for freesurfer output folder
#Enter BIDs input folder
#Processes multiple T1 runs
#Careful. Doesn't take into account T2 other than the first run... User should ckeck its quality
#No high-res processing so far though it could be done and may be preferable
#Dídac Macià Bros, 01-04-2019

#**************** USAGE ******************
#reconall_T1T2.sh -o SUBJECTS_DIR_FREESURFER -i BIDS_DIRECTORY -p num_parallel_cores
#/institut/processed_data/BBHI_output/batch_structural.sh -o /institut/processed_data/BBHI_output/structural -i /institut/processed_data/BBHI_structural -p 4
#*****************************************

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -o|--output_dir)
    SUBJECTS_DIR="$2"
    shift # past argument
    shift # past value
    ;;
    -i|--input_dir)
    BIDS_FOLDER="$2"
    shift # past argument
    shift # past value
    ;;
    -p|--pcores)
    PCORES="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done


#DEFAULT VALUES
PCORES=4

#gets params from terminal call
set -- "${POSITIONAL[@]}" # restore positional parameters

echo SUBJECT_DIR     = "${SUBJECTS_DIR}"
echo BIDS_DIR        = "${BIDS_FOLDER}"
echo PARALLEL CORES  = "${PCORES}"


#export SUBJECTS_DIR='/institut/processed_data/BBHI_output/structural'
#BIDS_FOLDER='/institut/processed_data/BBHI_structural'

for d in $BIDS_FOLDER/*/ ; do
    run_counter=0
    for nrun in $BIDS_FOLDER/$(basename $d)/ses-01/anat/$(basename $d)_ses-01_run-*_T1w.nii.gz ; do  
      run_counter=$((run_counter+1))
      if ((run_counter>1)) ; then
 SUBJECT_ID=$(basename $d)_run_$run_counter
 echo "REPEATED RUN num_$run_counter"
      else
 SUBJECT_ID=$(basename $d)
      fi
     
      if [ -e $SUBJECTS_DIR/$SUBJECT_ID ] ;then
 echo "$SUBJECT_ID is already processed. Skipping..."
      else
 echo "Processing $SUBJECT_ID ... with source image : $nrun"
 recon-all -all -s $SUBJECT_ID  -i $nrun -T2 $BIDS_FOLDER/$(basename $d)/ses-01/anat/$(basename $d)_ses-01_run-01_T2w.nii.gz -T2pial -openmp $PCORES -3T
      fi
    done
done

#-highres -expert $EXPERT_HIGHRES_FILE \ 
