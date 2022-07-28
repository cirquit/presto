#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}4.4 Creating CREAM plots...${normal}" 
cd ./plot-figures/cream-notebook
docker build -t cream-notebook:v1 .
echo "${bold}Docker Image built, starting the container...${normal}"
docker run -v $PRESTO_PATH:/root/presto/ \
           -v $CREAM_DATASET_PATH:/dataset/ \
           -v $TEMP_PATH:/tmp/ \
           -v $CREAM_LOG_PATH:/logs/ \
           -v $SUBMISSION_FIGURES_PATH:/submission/ \
           -it \
           cream-notebook:v1 
echo "${bold}-- Finished with creating all CREAM plots!${normal}"
