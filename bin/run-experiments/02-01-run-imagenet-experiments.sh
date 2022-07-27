#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}2.1.1 Running Imagenet experiments...${normal}" 
cd ./run-experiments/imagenet-experiments
docker build -t imagenet-experiments:v1 .
echo "${bold}Docker Image built, starting the container...${normal}"
docker run -v $PRESTO_PATH:/root/presto/ \
           -v $IMAGENET_DATASET_PATH:/dataset/ \
           -v $TEMP_PATH:/tmp/ \
           -v $IMAGENET_LOG_PATH:/logs/ \
           -v /proc/sys/vm/drop_caches:/drop_caches \
           -it \
           imagenet-experiments:v1 
echo "${bold}-- Finished with all imagenet experiments!${normal}"