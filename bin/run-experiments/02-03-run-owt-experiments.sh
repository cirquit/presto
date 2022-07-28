#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}2.3 Running OpenWebText experiments...${normal}" 
cd ./run-experiments/owt-experiments
docker build -t owt-experiments:v1 .
echo "${bold}Docker Image built, starting the container...${normal}"
docker run -v $PRESTO_PATH:/root/presto/ \
           -v $OWT_DATASET_PATH:/dataset/ \
           -v $TEMP_PATH:/tmp/ \
           -v $OWT_LOG_PATH:/logs/ \
           -v /proc/sys/vm/drop_caches:/drop_caches \
           -it \
           owt-experiments:v1 
echo "${bold}-- Finished with all OpenWebText experiments!${normal}"
