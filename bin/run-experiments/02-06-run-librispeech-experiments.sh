#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}2.6 Running Librispeech experiments...${normal}" 
cd ./run-experiments/librispeech-experiments
docker build -t librispeech-experiments:v1 .
echo "${bold}Docker Image built, starting the container...${normal}"
docker run -v $PRESTO_PATH:/root/presto/ \
           -v $LIBRISPEECH_DATASET_PATH:/dataset/ \
           -v $TEMP_PATH:/tmp/ \
           -v $LIBRISPEECH_LOG_PATH:/logs/ \
           -v /proc/sys/vm/drop_caches:/drop_caches \
           -it \
           librispeech-experiments:v1 
echo "${bold}-- Finished with all Librispeech experiments!${normal}"
