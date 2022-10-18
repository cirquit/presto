#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

URL_JPG="https://syncandshare.lrz.de/dl/fiAoYifVsQbB8cvYDQTwUB/cubepp-small-isenko-v3.zip"

echo "${bold}1.2.1 Downloading Cube++ dataset..."
echo "From: ${URL}"
echo "To: ${CUBEPP_DATASET_PATH}"
echo "---${normal}"

# downloading the JPG archive
wget -q --show-progress ${URL_JPG} --no-check-certificate -P ${CUBEPP_DATASET_PATH}

# downloading the PNG archives
# they forgot to upload the PNG0 archive on zenodo
#wget -q --show-progress https://storage.yandexcloud.net/cubepng0/PNG0.zip --no-check-certificate -P ${CUBEPP_DATASET_PATH}

#for ID in 1 2 3 4 5 6 7 8 9; do
#  URL="https://zenodo.org/record/4153431/files/PNG${ID}.zip"
#  wget -q --show-progress ${URL} --no-check-certificate -P ${CUBEPP_DATASET_PATH}
#done

echo "${bold}--- Finished downloading!"
echo "1.2.2 Extracting...${normal}"

cd ${CUBEPP_DATASET_PATH}
unzip cubepp-small-isenko-v3.zip
#for ID in 0; do
#  echo "Extracting ./PNG${ID}/Cube++/PNG to ./PNG"
#  unzip PNG${ID}.zip -d PNG${ID}
#done
echo "${bold}-- Finished extraction!"

echo "1.2.3 Removing compressed file...${normal}"
#rm JPG.zip PNG*.zip
rm *.zip
echo "${bold}-- Finished removing compressed dataset!${normal}"

#echo "${bold}1.2.4 Moving all .jpg/.png files in the corresponding directories...${normal}"

#mkdir -p JPG
#mv ./Cube++/JPG/*.jpg JPG/
#rm -r ./Cube++

#mkdir -p PNG
#for ID in 0; do
#  mv ./PNG${ID}/Cube++/PNG/*.png ./PNG/
#  rm -r ./PNG${ID}
#done
#echo "${bold}-- Finished moving all .jpg/.png files!${normal}"
