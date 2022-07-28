#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}2.4 Running CREAM experiments...${normal}" 
cd ./run-experiments/cream-experiments
docker build -t cream-experiments:v1 .
echo "${bold}Docker Image built, starting the container...${normal}"
docker run -v $PRESTO_PATH:/root/presto/ \
           -v $CREAM_DATASET_PATH:/dataset/ \
           -v $TEMP_PATH:/tmp/ \
           -v $CREAM_LOG_PATH:/logs/ \
           -v /proc/sys/vm/drop_caches:/drop_caches \
           -it \
           cream-experiments:v1 
echo "${bold}-- Finished with all CREAM experiments!${normal}"
