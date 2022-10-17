#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo "---"
echo "${bold}3.7 Combining synthetic logs...${normal}"

cd $SYNTHETIC_UINT8_LOG_PATH
$PRESTO_PATH/bin/concat-csv-logs.sh cum-df > full-log_cum-df.csv
echo "Created summarized cum-df log at: $SYNTHETIC_UINT8_LOG_PATH/full-log_cum-df.csv"
$PRESTO_PATH/bin/concat-csv-logs.sh cum-dstat-df > full-log_cum-dstat-df.csv
echo "Created summarized cum-dstat-df log at: $SYNTHETIC_UINT8_LOG_PATH/full-log_cum-dstat-df.csv"

cd $SYNTHETIC_FLOAT32_LOG_PATH
$PRESTO_PATH/bin/concat-csv-logs.sh cum-df > full-log_cum-df.csv
echo "Created summarized cum-df log at: $SYNTHETIC_FLOAT32_LOG_PATH/full-log_cum-df.csv"
$PRESTO_PATH/bin/concat-csv-logs.sh cum-dstat-df > full-log_cum-dstat-df.csv
echo "Created summarized cum-dstat-df log at: $SYNTHETIC_FLOAT32_LOG_PATH/full-log_cum-dstat-df.csv"

cd $SYNTHETIC_FLOAT32_SYS_LOG_PATH
$PRESTO_PATH/bin/concat-csv-logs.sh cum-df > full-log_cum-df.csv
echo "Created summarized cum-df log at: $SYNTHETIC_FLOAT32_SYS_LOG_PATH/full-log_cum-df.csv"
$PRESTO_PATH/bin/concat-csv-logs.sh cum-dstat-df > full-log_cum-dstat-df.csv
echo "Created summarized cum-dstat-df log at: $SYNTHETIC_FLOAT32_SYS_LOG_PATH/full-log_cum-dstat-df.csv"

cd $SYNTHETIC_FLOAT32_APP_LOG_PATH
$PRESTO_PATH/bin/concat-csv-logs.sh cum-df > full-log_cum-df.csv
echo "Created summarized cum-df log at: $SYNTHETIC_FLOAT32_APP_LOG_PATH/full-log_cum-df.csv"
$PRESTO_PATH/bin/concat-csv-logs.sh cum-dstat-df > full-log_cum-dstat-df.csv
echo "Created summarized cum-dstat-df log at: $SYNTHETIC_FLOAT32_APP_LOG_PATH/full-log_cum-dstat-df.csv"

cd $SYNTHETIC_FLOAT32_PARALLELISM_LOG_PATH
$PRESTO_PATH/bin/concat-csv-logs.sh cum-df > full-log_cum-df.csv
echo "Created summarized cum-df log at: $SYNTHETIC_FLOAT32_PARALLELISM_LOG_PATH/full-log_cum-df.csv"
$PRESTO_PATH/bin/concat-csv-logs.sh cum-dstat-df > full-log_cum-dstat-df.csv
echo "Created summarized cum-dstat-df log at: $SYNTHETIC_FLOAT32_PARALLELISM_LOG_PATH/full-log_cum-dstat-df.csv"

cd $SYNTHETIC_FLOAT32_TF_LOG_PATH
$PRESTO_PATH/bin/concat-csv-logs.sh cum-df > full-log_cum-df.csv
echo "Created summarized cum-df log at: $SYNTHETIC_FLOAT32_TF_LOG_PATH/full-log_cum-df.csv"
$PRESTO_PATH/bin/concat-csv-logs.sh cum-dstat-df > full-log_cum-dstat-df.csv
echo "Created summarized cum-dstat-df log at: $SYNTHETIC_FLOAT32_TF_LOG_PATH/full-log_cum-dstat-df.csv"

cd $SYNTHETIC_FLOAT32_NP_LOG_PATH
$PRESTO_PATH/bin/concat-csv-logs.sh cum-df > full-log_cum-df.csv
echo "Created summarized cum-df log at: $SYNTHETIC_FLOAT32_NP_LOG_PATH/full-log_cum-df.csv"
$PRESTO_PATH/bin/concat-csv-logs.sh cum-dstat-df > full-log_cum-dstat-df.csv
echo "Created summarized cum-dstat-df log at: $SYNTHETIC_FLOAT32_NP_LOG_PATH/full-log_cum-dstat-df.csv"

echo "${bold}-- Finished summarizing synthetic logs!${normal}"
