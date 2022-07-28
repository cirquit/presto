#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}2.7 Running synthetic experiments...${normal}" 
cd ./run-experiments/synthetic-experiments
docker build -t synthetic-experiments:v1 .
echo "${bold}Docker Image built, starting the container...${normal}"
docker run -v $PRESTO_PATH:/root/presto/ \
           -v $TEMP_PATH:/tmp/ \
           -v $SYNTHETIC_LOG_PATH:/logs/ \
           -v /proc/sys/vm/drop_caches:/drop_caches \
           -it \
           synthetic-experiments:v1 
echo "${bold}-- Finished with all synthetic experiments!${normal}"
