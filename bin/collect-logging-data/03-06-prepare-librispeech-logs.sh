#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}3.6 Combining Librispeech logs...${normal}"
cd $LIBRISPEECH_LOG_PATH
$PRESTO_PATH/bin/concat-csv-logs.sh cum-df > full-log_cum-df.csv
echo "Created summarized cum-df log at: $LIBRISPEECH_LOG_PATH/full-log_cum-df.csv"
$PRESTO_PATH/bin/concat-csv-logs.sh cum-dstat-df > full-log_cum-dstat-df.csv
echo "Created summarized cum-dstat-df log at: $LIBRISPEECH_LOG_PATH/full-log_cum-dstat-df.csv"

echo "${bold}-- Finished summarizing Librispeech logs!${normal}"
