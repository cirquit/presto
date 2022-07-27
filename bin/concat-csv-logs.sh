#!/bin/bash

# usage: ./concat-csv-log-files.sh [cum-df,cum-dstat-df] > newfile.csv

CSV_FILES_SH="ls | grep csv | grep $1 | grep -v full"
FILES=$(eval $CSV_FILES_SH)
  
FIRST_FILE=$(echo $FILES | cut --delimiter " " --fields 1)
CSV_HEADER=$(head -n 1 $FIRST_FILE)

# insert header once at the start
echo $CSV_HEADER

for FILE in $FILES
do
    # cut header from each file
    sed '1d' $FILE
done
