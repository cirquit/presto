#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}1.1.1 Downloading Imagenet...${normal} (~ 30min)" 
echo "---"
read -p "Docker is installed and available without sudo? ${bold}Confim.${normal}" choice
read -p "Kaggle credentials (kaggle.json) are in ${bold}(...)/presto/bin/kaggle.json? Confirm.${normal}" choice
echo "---"
echo "Starting docker container to download the
https://www.kaggle.com/competitions/imagenet-object-localization-challenge/data dataset"

cp kaggle.json ./download-datasets/imagenet-docker/kaggle.json
cd ./download-datasets/imagenet-docker/
docker build -t kaggle-imagenet-downloader:v1 .
docker run -v $IMAGENET_DATASET_PATH:/tmp/ kaggle-imagenet-downloader:v1 

echo "${bold}1.1.2 Extracting...${normal} (~ 1-2h)"

cd ${IMAGENET_DATASET_PATH}
unzip imagenet-object-localization-challenge.zip
echo "${bold}-- Finished extraction!"


echo "${bold}1.1.4 Removing compressed files...${normal}"
rm imagenet-object-localization-challenge.zip
echo "${bold}-- Finished removing compressed dataset!${normal}"
