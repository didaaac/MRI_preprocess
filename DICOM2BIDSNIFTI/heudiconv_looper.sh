#This is batch helps transforming from DICOM to BIDs nifti selected sequences as long as they do not exist in a target FOLDER
#source activate python2_7
TARGET_FOLDER=''
OUTPUT_FOLDER='/institut/processed_data/BBHI_structural'
DICOM_INPUT_FOLDER='/institut/BBHI_DICOMS'
SESSION_NUM='01'

SEQUENCES="T1w_MPR T2w_SPC FLAIR"
EXPORT_BIDS_KEY=("T1w" "T2w" "FLAIR")

list_subs=$(ls $DICOM_INPUT_FOLDER/* -d)
echo $list_subs

for i in $list_subs; do
  inde=0
  for sequ in $SEQUENCES; do
  inde=$((inde+1))
  echo $sequ
  SUBJECT_ID=$(basename $i)
  echo "processing subject $SUBJECT_ID..."
  echo $DICOM_INPUT_FOLDER/{subject}/$sequ/*IMA
  TARGET_FILE="$OUTPUT_FOLDER/sub-${SUBJECT_ID}/ses-${SESSION_NUM}/anat/sub-${SUBJECT_ID}_ses-${SESSION_NUM}_run-01_${EXPORT_BIDS_KEY[($inde)]}.nii.gz"
  if [ -e $TARGET_FILE ] 
	then
	  echo "$SUBJECT_ID already transformed. Skipping..."
	else
	  echo "Transforming $SUBJECT_ID ..."
	  #echo "$DICOM_INPUT_FOLDER/{subject}/$sequ/*IMA"
	 heudiconv "-d $DICOM_INPUT_FOLDER/{subject}/$sequ/*IMA -s $SUBJECT_ID -ss $SESSION_NUM -f /home/didac/Scripts/dicom2BIDS/convert_BBHI.py  -c dcm2niix -b -o $OUTPUT_FOLDER"	  
      fi
  done
done

