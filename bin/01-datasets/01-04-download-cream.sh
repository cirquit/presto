#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

URL="https://dataserv.ub.tum.de/s/m1554766/download"

echo "${bold}1.4.1 Downloading CREAM dataset..."
echo "From: ${URL}"
echo "To: ${CREAM_DATASET_PATH}"
echo "---${normal}"

wget -q --show-progress ${URL} --no-check-certificate -O ${CREAM_DATASET_PATH}/cream-full.zip

echo "${bold}--- Finished downloading!"
echo "1.4.2 Extracting...${normal}"

cd ${CREAM_DATASET_PATH}
unzip cream-full.zip 
echo "${bold}-- Finished extraction!"

echo "1.4.3 Removing compressed file...${normal}"
rm cream-full.zip
echo "${bold}-- Finished removing compressed dataset!${normal}"
