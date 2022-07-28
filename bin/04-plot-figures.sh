#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

if [ -z ${PRESTO_PATH+x} ]; then                                                                         
   echo "${bold}Error:${normal} PRESTO_PATH is not set"
   echo "Please run \"source 00-environment-variables.sh\""
   exit 1
fi

imagenet=0
cubepp=0
owt=0
cream=0
commonvoice=0
librispeech=0
synthetic=0

run_all_experiments()
{
    imagenet=1; cubepp=1; owt=1; cream=1;
    commonvoice=1; librispeech=1; synthetic=1;
}

while [ -n "$1" ]
do
case "$1" in
    all)         echo "Preparing data for all experiments..."; run_all_experiments; break ;;
    imagenet)    echo "Preparing imagenet..."; imagenet=1;;
    cubepp)      echo "Preparing cubepp..."; cubepp=1 ;;
    owt)         echo "Preparing owt..."; owt=1 ;;
    cream)       echo "Preparing cream..."; cream=1;;
    commonvoice) echo "Preparing commonvoice..."; commonvoice=1 ;;
    librispeech) echo "Preparing librispeech..."; librispeech=1 ;;
    synthetic)   echo "Preparing synthetic..."; synthetic=1 ;;
    *) echo "$1 is not an option"; break ;;
esac
shift
done

if [[ $imagenet -eq 1 ]]; then
  ./plot-figures/04-01-create-imagenet-plots.sh
fi
if [[ $cubepp -eq 1 ]]; then
  ./plot-figures/04-02-create-cubepp-plots.sh
fi
if [[ $owt -eq 1 ]]; then
  ./plot-figures/04-03-create-owt-plots.sh
fi
if [[ $cream -eq 1 ]]; then
  ./plot-figures/04-04-create-cream-plots.sh
fi
if [[ $commonvoice -eq 1 ]]; then
  ./plot-figures/04-05-create-commonvoice-plots.sh
fi
if [[ $librispeech -eq 1 ]]; then
  ./plot-figures/04-06-create-librispeech-plots.sh
fi
if [[ $synthetic -eq 1 ]]; then
  ./plot-figures/04-07-create-synthetic-plots.sh
fi

