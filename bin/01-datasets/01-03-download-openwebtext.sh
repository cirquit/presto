#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "1.3.1 Downloading openwebtext..." 
echo "---"
echo "Google Drive is being a PITA to work with - click on this link and save the dataset to
${bold}${OWT_DATASET_PATH}${normal}."

echo "---"
echo "https://drive.google.com/file/d/1EA5V0oetDCOke7afsktL_JDQ-ETtNOvx/view?usp=sharing"
echo "---"
read -p "Downloaded? Confirm to move forward." choice

echo "1.3.2 Extracting...${normal}"

cd ${OWT_DATASET_PATH}
tar xf openwebtext.tar.xz
echo "${bold}-- Finished extraction!"

echo "1.3.3 Removing compressed file...${normal}"
# rm openwebtext.tar.xz
echo "${bold}-- Finished removing compressed dataset!${normal}"
