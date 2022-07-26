#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

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
  ./02-experiments/02-01-run-imagenet-experiments.sh    
fi

#echo $imagenet
#echo $cubepp
#echo $owt
#echo $cream
#echo $commonvoice
#echo $librispeech
#echo $synthetic


# ./01-datasets/01-01-download-imagenet.sh

# ./01-datasets/01-02-download-cube++.sh

# ./01-datasets/01-03-download-openwebtext.sh

# ./01-datasets/01-04-download-cream.sh

# ./01-datasets/01-05-download-commonvoice.sh

# ./01-datasets/01-06-download-librispeech.sh
