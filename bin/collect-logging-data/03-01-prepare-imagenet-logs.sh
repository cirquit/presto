#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}3.1 Combining imagenet logs...${normal}"
cd $IMAGENET_LOG_PATH
$PRESTO_PATH/bin/concat-csv-logs.sh cum-df > full-log_cum-df.csv
echo "Created summarized cum-df log at: $IMAGENET_LOG_PATH/full-log_cum-df.csv"
$PRESTO_PATH/bin/concat-csv-logs.sh cum-dstat-df > full-log_cum-dstat-df.csv
echo "Created summarized cum-dstat-df log at: $IMAGENET_LOG_PATH/full-log_cum-dstat-df.csv"

cd $IMAGENET_BEFORE_CENTERING_LOG_PATH
$PRESTO_PATH/bin/concat-csv-logs.sh cum-df > full-log_cum-df.csv
echo "Created summarized cum-df log at: $IMAGENET_LOG_PATH/before-centering/full-log_cum-df.csv"
$PRESTO_PATH/bin/concat-csv-logs.sh cum-dstat-df > full-log_cum-dstat-df.csv
echo "Created summarized cum-dstat-df log at: $IMAGENET_LOG_PATH/before-centering/full-log_cum-dstat-df.csv"

cd $IMAGENET_AFTER_CENTERING_LOG_PATH
$PRESTO_PATH/bin/concat-csv-logs.sh cum-df > full-log_cum-df.csv
echo "Created summarized cum-df log at: $IMAGENET_LOG_PATH/after-centering/full-log_cum-df.csv"
$PRESTO_PATH/bin/concat-csv-logs.sh cum-dstat-df > full-log_cum-dstat-df.csv
echo "Created summarized cum-dstat-df log at: $IMAGENET_LOG_PATH/after-centering/full-log_cum-dstat-df.csv"


echo "${bold}-- Finished summarizing imagenet logs!${normal}"
