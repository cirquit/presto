#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "1.3.1 Downloading openwebtext..." 
echo "---"
echo "Google Drive does not want to allow automatic downloads...please click on this link and save the dataset to ${bold}${OWT_DATASET_PATH}/openwebtext_180k.zip${normal}."

echo "---"
echo "https://drive.google.com/file/d/19l3B6HAfpQddGJZa6ZY0HadAhrwjRtfK/view?usp=sharing"
echo "---"
read -p "Downloaded? Confirm to move forward." choice

echo "1.3.2 Extracting...${normal}"

cd ${OWT_DATASET_PATH}
unzip openwebtext_180k.zip
echo "${bold}-- Finished extraction!"

echo "1.3.3 Removing compressed file...${normal}"
# rm openwebtext_180k.zip
echo "${bold}-- Finished removing compressed dataset!${normal}"
