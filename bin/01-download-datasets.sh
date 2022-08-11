#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

if [ -z ${PRESTO_PATH+x} ]; then
  echo "${bold}Error:${normal} PRESTO_PATH is not set"
  echo "Please run \"source 00-environment-variables.sh\""
  exit 1
fi


echo "${bold}1. Downloading the following datasets${normal}"
echo " - 1.1 ILSVRC2012  - 309.0GB compressed + 157.0GB uncompressed - docker"
echo " - 1.2 Cube++      -  84.0GB compressed +  84.5GB uncompressed - bash"
echo " - 1.3 OpenWebText -   1.5GB compressed +   7.3GB uncompressed - bash"
echo " - 1.4 CREAM       - 103.6GB compressed +   104GB uncompressed - bash"
echo " - 1.5 Commonvoice -   0.9GB compressed +   0.9GB uncompressed - bash"
echo " - 1.6 LibriSpeech -   5.9GB compressed +   6.2GB uncompressed - bash"
echo "Total space requirement: ${bold}~ 870GB${normal} to ${bold}DATASETS_PATH=${DATASETS_PATH}${normal}"
echo "Compressed datasets are deleted after the download, resulting in ${bold}360GB${normal} storage consumption"

./download-datasets/01-01-download-imagenet.sh

./download-datasets/01-02-download-cube++.sh

./download-datasets/01-03-download-openwebtext.sh

./download-datasets/01-04-download-cream.sh

./download-datasets/01-05-download-commonvoice.sh

./download-datasets/01-06-download-librispeech.sh

echo "${bold}Finished downloading all datasets!${normal}"

