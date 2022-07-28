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
    all)         echo "Running all experiments..."; run_all_experiments; break ;;
    imagenet)    echo "Running imagenet..."; imagenet=1;;
    cubepp)      echo "Running cubepp..."; cubepp=1 ;;
    owt)         echo "Running owt..."; owt=1 ;;
    cream)       echo "Running cream..."; cream=1;;
    commonvoice) echo "Running commonvoice..."; commonvoice=1 ;;
    librispeech) echo "Running librispeech..."; librispeech=1 ;;
    synthetic)   echo "Running synthetic..."; synthetic=1 ;;
    *) echo "$1 is not an option"; break ;;
esac
shift
done

if [[ $imagenet -eq 1 ]]; then
  ./run-experiments/02-01-run-imagenet-experiments.sh    
fi

if [[ $cubepp -eq 1 ]]; then
  ./run-experiments/02-02-run-cubepp-experiments.sh    
fi

if [[ $owt -eq 1 ]]; then
  ./run-experiments/02-03-run-owt-experiments.sh    
fi

if [[ $cream -eq 1 ]]; then
  ./run-experiments/02-04-run-cream-experiments.sh    
fi

if [[ $commonvoice -eq 1 ]]; then
  ./run-experiments/02-05-run-commonvoice-experiments.sh    
fi

if [[ $librispeech -eq 1 ]]; then
  ./run-experiments/02-06-run-librispeech-experiments.sh    
fi

if [[ $synthetic -eq 1 ]]; then
  ./run-experiments/02-07-run-synthetic-experiments.sh    
fi
