export DATASETS_PATH="/mnt/ceph-storage/temp/isenko/temp"
export TEMP_PATH="/mnt/ceph-storage/temp/isenko/temp"
export LOG_PATH="/mnt/ceph-storage/temp/isenko/temp"
export SUBMISSION_FIGURES_PATH="/mnt/ceph-storage/temp/isenko/temp"

export IMAGENET_DATASET_PATH="${DATASETS_PATH}/imagenet"
mkdir -p ${IMAGENET_DATASET_PATH}

export CUBEPP_DATASET_PATH="${DATASETS_PATH}/cube++"
mkdir -p ${CUBEPP_DATASET_PATH}

export OWT_DATASET_PATH="${DATASETS_PATH}/openwebtext"
mkdir -p ${OWT_DATASET_PATH}

export CREAM_DATASET_PATH="${DATASETS_PATH}/cream"
mkdir -p ${CREAM_DATASET_PATH}

export COMMONVOICE_DATASET_PATH="${DATASETS_PATH}/commonvoice"
mkdir -p ${COMMONVOICE_DATASET_PATH}

export LIBRISPEECH_DATASET_PATH="${DATASETS_PATH}/librispeech"
mkdir -p ${LIBRISPEECH_DATASET_PATH}

