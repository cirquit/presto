#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

if [ -z ${PRESTO_PATH+x} ]; then                                                                         
   echo "${bold}Error:${normal} PRESTO_PATH is not set"
   echo "Please run \"source 00-environment-variables.sh\""
   exit 1
fi

logs=0
datasets=0
temp=0

delete_all()
{
    logs=1; datasets=1; artefacts=1;
    
}

while [ -n "$1" ]
do
case "$1" in
    all)       echo "Deleting everything (logs, datasets, temp)..."; delete_all; break ;;
    logs)      echo "Deleting logs..."; logs=1 ;;
    datasets)  echo "Deleting datasets..."; datasets=1 ;;
    temp) echo "Deleting temp..."; temp=1 ;;
    *) echo "$1 is not an option"; break ;;
esac
shift
done

if [[ $logs -eq 1 ]]; then
  read -p "Running 'rm -rf' on path '$LOG_PATH'. Confirm [yn]: " confirm
  case $confirm in
    [Yy]* ) rm -rf $LOG_PATH;;
    [Nn]* ) exit;;
    * ) echo "Please answer yes or no.";;
  esac
fi

if [[ $datasets -eq 1 ]]; then
  read -p "Running 'rm -rf' on path '$DATASETS_PATH'. Confirm [yn]: " confirm
  case $confirm in
    [Yy]* ) rm -rf $DATASETS_PATH;;
    [Nn]* ) exit;;
    * ) echo "Please answer yes or no.";;
  esac
fi

if [[ $temp -eq 1 ]]; then
  read -p "Running 'rm -rf' on path '$TEMP_PATH'. Confirm [yn]: " confirm
  case $confirm in
    [Yy]* ) sudo rm -rf $TEMP_PATH;;
    [Nn]* ) exit;;
    * ) echo "Please answer yes or no.";;
  esac

fi

