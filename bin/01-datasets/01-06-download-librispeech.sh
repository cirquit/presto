#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

URL="https://openslr.elda.org/resources/12/train-clean-100.tar.gz"

echo "${bold}1.6.1 Downloading Librispeech TRAIN_CLEAN_100..."
echo "From: ${URL}"
echo "To: ${LIBRISPEECH_DATASET_PATH}"
echo "---${normal}"

wget -q --show-progress https://openslr.elda.org/resources/12/train-clean-100.tar.gz -P ${LIBRISPEECH_DATASET_PATH}

echo "${bold}--- Finished downloading!"
echo "1.6.2 Extracting...${normal}"

cd $LIBRISPEECH_DATASET_PATH
tar xzf train-clean-100.tar.gz
echo "${bold}-- Finished extraction!"

echo "1.6.3 Removing compressed file...${normal}"
rm train-clean-100.tar.gz
echo "${bold}-- Finished removing compressed dataset!${normal}"
