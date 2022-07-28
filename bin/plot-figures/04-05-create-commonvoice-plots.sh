#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}4.5 Creating Commonvoice plots...${normal}" 
cd ./plot-figures/commonvoice-notebook
docker build -t commonvoice-notebook:v1 .
echo "${bold}Docker Image built, starting the container...${normal}"
docker run -v $PRESTO_PATH:/root/presto/ \
           -v $COMMONVOICE_DATASET_PATH:/dataset/ \
           -v $TEMP_PATH:/tmp/ \
           -v $COMMONVOICE_LOG_PATH:/logs/ \
           -v $SUBMISSION_FIGURES_PATH:/submission/ \
           -it \
           commonvoice-notebook:v1 
echo "${bold}-- Finished with creating all Commonvoice plots!${normal}"
