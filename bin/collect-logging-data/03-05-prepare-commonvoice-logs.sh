#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}3.5 Combining Commonvoice logs...${normal}"
cd $COMMONVOICE_LOG_PATH
$PRESTO_PATH/bin/concat-csv-logs.sh cum-df > full-log_cum-df.csv
echo "Created summarized cum-df log at: $COMMONVOICE_LOG_PATH/full-log_cum-df.csv"
$PRESTO_PATH/bin/concat-csv-logs.sh cum-dstat-df > full-log_cum-dstat-df.csv
echo "Created summarized cum-dstat-df log at: $COMMONVOICE_LOG_PATH/full-log_cum-dstat-df.csv"

echo "${bold}-- Finished summarizing Commonvoice logs!${normal}"
