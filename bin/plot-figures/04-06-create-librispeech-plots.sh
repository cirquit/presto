#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}4.6 Creating Librispeech plots...${normal}" 
cd ./plot-figures/librispeech-notebook
docker build -t librispeech-notebook:v1 .
echo "${bold}Docker Image built, starting the container...${normal}"
docker run -v $PRESTO_PATH:/root/presto/ \
           -v $LIBRISPEECH_DATASET_PATH:/dataset/ \
           -v $TEMP_PATH:/tmp/ \
           -v $LIBRISPEECH_LOG_PATH:/logs/ \
           -v $SUBMISSION_FIGURES_PATH:/submission/ \
           -it \
           librispeech-notebook:v1 
echo "${bold}-- Finished with creating all Librispeech plots!${normal}"
