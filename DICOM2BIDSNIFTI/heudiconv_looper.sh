#This is batch helps transforming from DICOM to BIDs nifti selected sequences as long as they do not exist in a target FOLDER
source activate python2_7
TARGET_FOLDER=''
OUTPUT_FOLDER='/institut/processed_data/BBHI_structural2'
DICOM_INPUT_FOLDER='/institut/BBHI_DICOMS'
SESSION_NUM='01'


list_subs=$(ls $DICOM_INPUT_FOLDER/* -d)
echo $list_subs

for i in $list_subs; do
  inde=0
  inde=$((inde+1))
  echo $sequ
  SUBJECT_ID=$(basename $i)
  echo "processing subject $SUBJECT_ID..."
  echo $DICOM_INPUT_FOLDER/{subject}/*/*IMA
  heudiconv -d $DICOM_INPUT_FOLDER/{subject}/*/*IMA -s $SUBJECT_ID -ss $SESSION_NUM -f convert_BBHI_structural.py -c dcm2niix -b -o $OUTPUT_FOLDER	  
done

conda deactivate
