# input - all the log files which were created by repeat-experiment.sh
# usage: ./concat-csv-log-files.sh file1.csv file2.csv > newfile.csv

# create header, should be the same with all files
head "$1" -n 1
# get data
for file in "$@"
do
  sed '1d' $file
done
