#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}2.2 Running Cube++ experiments...${normal}" 
cd ./run-experiments/cubepp-experiments
docker build -t cubepp-experiments:v1 .
echo "${bold}Docker Image built, starting the container...${normal}"
docker run -v $PRESTO_PATH:/root/presto/ \
           -v $CUBEPP_DATASET_PATH:/dataset/ \
           -v $TEMP_PATH:/tmp/ \
           -v $CUBEPP_LOG_PATH:/logs/ \
           -v /proc/sys/vm/drop_caches:/drop_caches \
           -it \
           cubepp-experiments:v1 
echo "${bold}-- Finished with all cubepp experiments!${normal}"
