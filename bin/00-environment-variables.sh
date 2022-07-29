# !! modify me
export PRESTO_PATH="/home/ubuntu/presto"
# !! modify me
export DATASETS_PATH="/mnt/ceph-storage/temp/isenko/temp"
mkdir -p $DATASETS_PATH
# !! modify me
export TEMP_PATH="/mnt/ceph-storage/temp/isenko/temp/strategies"
mkdir -p $TEMP_PATH
# !! modify me
export LOG_PATH="/mnt/ceph-storage/temp/isenko/temp/logs"
mkdir -p $LOG_PATH

# ---- no modification from this point onwards

# based on the repository structure
export SUBMISSION_FIGURES_PATH="$PRESTO_PATH/paper/figures"

# create dataset paths
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

# create log paths
export IMAGENET_LOG_PATH="${LOG_PATH}/imagenet"
mkdir -p ${IMAGENET_LOG_PATH}
export IMAGENET_BEFORE_CENTERING_LOG_PATH="${LOG_PATH}/imagenet/before-centering"
mkdir -p ${IMAGENET_BEFORE_CENTERING_LOG_PATH}
export IMAGENET_AFTER_CENTERING_LOG_PATH="${LOG_PATH}/imagenet/after-centering"
mkdir -p ${IMAGENET_AFTER_CENTERING_LOG_PATH}
export CUBEPP_LOG_PATH="${LOG_PATH}/cube++"
mkdir -p ${CUBEPP_LOG_PATH}
export CUBEPP_PNG_LOG_PATH="${LOG_PATH}/cube++/png"
mkdir -p ${CUBEPP_PNG_LOG_PATH}
export CUBEPP_JPG_LOG_PATH="${LOG_PATH}/cube++/jpg"
mkdir -p ${CUBEPP_JPG_LOG_PATH}
export OWT_LOG_PATH="${LOG_PATH}/openwebtext"
mkdir -p ${OWT_LOG_PATH}
export CREAM_LOG_PATH="${LOG_PATH}/cream"
mkdir -p ${CREAM_LOG_PATH}
export COMMONVOICE_LOG_PATH="${LOG_PATH}/commonvoice"
mkdir -p ${COMMONVOICE_LOG_PATH}
export LIBRISPEECH_LOG_PATH="${LOG_PATH}/librispeech"
mkdir -p ${LIBRISPEECH_LOG_PATH}
export SYNTHETIC_LOG_PATH="${LOG_PATH}/synthetic"
mkdir -p ${SYNTHETIC_LOG_PATH}

export SYNTHETIC_UINT8_LOG_PATH="${SYNTHETIC_LOG_PATH}/uint8"
mkdir -p ${SYNTHETIC_UINT8_LOG_PATH}
export SYNTHETIC_FLOAT32_LOG_PATH="${SYNTHETIC_LOG_PATH}/float32"
mkdir -p ${SYNTHETIC_FLOAT32_LOG_PATH}
export SYNTHETIC_FLOAT32_SYS_LOG_PATH="${SYNTHETIC_FLOAT32_LOG_PATH}/sys-caching"
mkdir -p ${SYNTHETIC_FLOAT32_SYS_LOG_PATH}
export SYNTHETIC_FLOAT32_APP_LOG_PATH="${SYNTHETIC_FLOAT32_LOG_PATH}/app-caching"
mkdir -p ${SYNTHETIC_FLOAT32_APP_LOG_PATH}
export SYNTHETIC_FLOAT32_PARALLELISM_LOG_PATH="${SYNTHETIC_FLOAT32_LOG_PATH}/parallelism"
mkdir -p ${SYNTHETIC_FLOAT32_PARALLELISM_LOG_PATH}
export SYNTHETIC_FLOAT32_TF_LOG_PATH="${SYNTHETIC_FLOAT32_LOG_PATH}/tensorflow"
mkdir -p ${SYNTHETIC_FLOAT32_TF_LOG_PATH}
export SYNTHETIC_FLOAT32_NP_LOG_PATH="${SYNTHETIC_FLOAT32_LOG_PATH}/numpy"
mkdir -p ${SYNTHETIC_FLOAT32_NP_LOG_PATH}

