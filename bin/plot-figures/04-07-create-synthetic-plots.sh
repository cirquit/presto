#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}4.7 Creating synthetic plots...${normal}" 
cd ./plot-figures/synthetic-notebook
docker build -t synthetic-notebook:v1 .
echo "${bold}Docker Image built, starting the container...${normal}"
docker run -v $PRESTO_PATH:/root/presto/ \
           -v $TEMP_PATH:/tmp/ \
           -v $SYNTHETIC_LOG_PATH:/logs/ \
           -v $SUBMISSION_FIGURES_PATH:/submission/ \
           -it \
           synthetic-notebook:v1 
echo "${bold}-- Finished with creating all synthetic plots!${normal}"
