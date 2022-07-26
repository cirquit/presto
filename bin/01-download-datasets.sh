#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "${bold}1. Downloading the following datasets${normal}"
echo " - 1.1 ILSVRC2012  - 309.0GB compressed + 157.0GB uncompressed - via docker"
echo " - 1.2 Cube++      -  84.0GB compressed +  84.5GB uncompressed - automatic"
echo " - 1.3 OpenWebText -   1.5GB compressed +   7.3GB - manual"
echo " - 1.4 CREAM       - 103.6GB compressed +  TODOGB - automatic"
echo " - 1.5 Commonvoice -   0.9GB compressed +   0.9GB - manual"
echo " - 1.6 LibriSpeech -   5.9GB compressed +   6.2GB - automatic"
echo "Total space requirement: ${bold} ~1TB ${normal}to ${bold}DATASETS_PATH=${DATASETS_PATH}${normal}"

export IMAGENET_DATASET_PATH="${DATASETS_PATH}/imagenet"
mkdir -p ${IMAGENET_DATASET_PATH}
# ./01-datasets/01-01-download-imagenet.sh

export CUBEPP_DATASET_PATH="${DATASETS_PATH}/cube++"
mkdir -p ${CUBEPP_DATASET_PATH}
# ./01-datasets/01-02-download-cube++.sh

export OWT_DATASET_PATH="${DATASETS_PATH}/openwebtext"
mkdir -p ${OWT_DATASET_PATH}
# ./01-datasets/01-03-download-openwebtext.sh

export CREAM_DATASET_PATH="${DATASETS_PATH}/cream"
mkdir -p ${CREAM_DATASET_PATH}
# ./01-datasets/01-04-download-cream.sh

export COMMONVOICE_DATASET_PATH="${DATASETS_PATH}/commonvoice"
mkdir -p ${COMMONVOICE_DATASET_PATH}
# ./01-datasets/01-05-download-commonvoice.sh

export LIBRISPEECH_DATASET_PATH="${DATASETS_PATH}/librispeech"
mkdir -p ${LIBRISPEECH_DATASET_PATH}
# ./01-datasets/01-06-download-librispeech.sh

echo "${bold}Finished downloading all datasets!"

