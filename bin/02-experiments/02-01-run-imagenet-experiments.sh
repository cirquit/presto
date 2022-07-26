#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}2.1.1 Running Imagenet experiments...${normal}" 
cd ./02-experiments/imagenet-experiments
docker build -t imagenet-experiments:v1 .
docker run -v $PRESTO_PATH:/root/ \
           -v $IMAGENET_DATASET_PATH:/dataset/ \
           -v $TEMP_PATH:/tmp/ \
           -v $LOG_PATH:/log/ imagenet-experiments:v1 

echo "${bold}-- Finished with all imagenet experiments!${normal}"