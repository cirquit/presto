#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}4.2 Creating OpenWebText plots...${normal}" 
cd ./plot-figures/owt-notebook
docker build -t owt-notebook:v1 .
echo "${bold}Docker Image built, starting the container...${normal}"
docker run -v $PRESTO_PATH:/root/presto/ \
           -v $OWT_DATASET_PATH:/dataset/ \
           -v $TEMP_PATH:/tmp/ \
           -v $OWT_LOG_PATH:/logs/ \
           -v $SUBMISSION_FIGURES_PATH:/submission/ \
           -it \
           owt-notebook:v1 
echo "${bold}-- Finished with creating all OpenWebText plots!${normal}"
