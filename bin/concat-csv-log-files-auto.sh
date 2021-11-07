#!/bin/zsh

# usage: ./concat-csv-log-files.sh [cum-df,cum-dstat-df] > newfile.csv

CSV_FILES_SH="ls | grep csv | grep $1"
FILES=$(eval $CSV_FILES_SH)
  
FIRST_FILE=$(echo $FILES | head -n 1)
CSV_HEADER=$(head -n 1 $FIRST_FILE)

# insert header once at the start
echo $CSV_HEADER

for FILE in *$1*.csv
do
    # cut header from each file
    sed '1d' $FILE
    #echo $FILE
done
