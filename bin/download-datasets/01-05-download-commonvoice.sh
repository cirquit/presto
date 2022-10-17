#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "1.5.1 Downloading commonvoice 5.1 singleword english..."
echo "---"
URL=https://syncandshare.lrz.de/dl/fiHrUgNaoGQC5yWFg916sZyP/commonvoice-5.1-single-word-english.tar.gz
echo "From: ${URL}"
echo "To: ${COMMONVOICE_DATASET_PATH}"
echo "---${normal}"

# downloading the JPG archive
wget -q --show-progress ${URL} -P ${COMMONVOICE_DATASET_PATH}
echo "${bold}-- Finished downloading!"
#echo "Google Drive does not want to allow automatic downloads...please click on this link and save the dataset to ${bold}${COMMONVOICE_DATASET_PATH}${normal}."

#echo "---"
#echo "https://drive.google.com/file/d/1Ty4gTQaBOqLZWnaagR9HBW3nN1_Ud1V5/view?usp=sharing"
#echo "---"
#read -p "Downloaded? Confirm to move forward." choice

echo "1.5.2 Extracting...${normal}"

cd ${COMMONVOICE_DATASET_PATH}
tar xzf commonvoice-5.1-single-word-english.tar.gz
echo "${bold}-- Finished extraction!"

echo "1.5.3 Removing compressed file...${normal}"
rm commonvoice-5.1-single-word-english.tar.gz
echo "${bold}-- Finished removing compressed dataset!${normal}"
