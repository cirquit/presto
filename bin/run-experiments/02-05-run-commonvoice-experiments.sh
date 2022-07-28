#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}2.5 Running Commonvoice experiments...${normal}" 
cd ./run-experiments/commonvoice-experiments
docker build -t commonvoice-experiments:v1 .
echo "${bold}Docker Image built, starting the container...${normal}"
docker run -v $PRESTO_PATH:/root/presto/ \
           -v $COMMONVOICE_DATASET_PATH:/dataset/ \
           -v $TEMP_PATH:/tmp/ \
           -v $COMMONVOICE_LOG_PATH:/logs/ \
           -v /proc/sys/vm/drop_caches:/drop_caches \
           -it \
           commonvoice-experiments:v1 
echo "${bold}-- Finished with all Commonvoice experiments!${normal}"
