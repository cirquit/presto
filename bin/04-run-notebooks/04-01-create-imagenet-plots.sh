#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}4.1 Creating Imagenet plots...${normal}" 
cd ./04-run-notebooks/imagenet-notebook
docker build -t imagenet-notebook:v1 .
echo "${bold}Docker Image built, starting the container...${normal}"
docker run -v $PRESTO_PATH:/root/presto/ \
           -v $IMAGENET_DATASET_PATH:/dataset/ \
           -v $TEMP_PATH:/tmp/ \
           -v $IMAGENET_LOG_PATH:/logs/ \
           -v $SUBMISSION_FIGURES_PATH:/submission/ \
           -it \
           imagenet-notebook:v1 
echo "${bold}-- Finished with creating all imagenet plots!${normal}"
