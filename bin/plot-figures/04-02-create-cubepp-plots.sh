#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}4.2 Creating Cube++ plots...${normal}" 
cd ./plot-figures/cubepp-notebook
docker build -t cubepp-notebook:v1 .
echo "${bold}Docker Image built, starting the container...${normal}"
docker run -v $PRESTO_PATH:/root/presto/ \
           -v $CUBEPP_DATASET_PATH:/dataset/ \
           -v $TEMP_PATH:/tmp/ \
           -v $CUBEPP_LOG_PATH:/logs/ \
           -v $SUBMISSION_FIGURES_PATH:/submission/ \
           -it \
           cubepp-notebook:v1 
echo "${bold}-- Finished with creating all Cube++ plots!${normal}"
