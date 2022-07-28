#!/bin/bash

pythonscript="cubeplusplus_demo.py"

echo "---"
echo "I. Starting with short parallelism experiments..."
echo "---"
# 1.1 Parallelism experiments + caching
for threadcount in 1 2 4 8
do
  for pipelinemod in jpg png
  do
    echo 3 > /drop_caches
    compression="none"
    samplecount=4890
    runs=2
    python -u $pythonscript $threadcount $compression $samplecount $runs $pipelinemod
  done
done
# 1.2 clean up
rm -rf /tmp/cubeplusplus*

echo "---"
echo "II. Compression experiments..."
echo "---"
# 3.1 Compression experiments
for compression in ZLIB GZIP
do
  for pipelinemod in jpg png
  do
    echo 3 > /drop_caches
    threadcount=8
    samplecount=4890
    runs=1
    python -u $pythonscript $threadcount $compression $samplecount $runs $pipelinemod
  done
done
# 3.2 Clean up
rm -rf /tmp/cubeplusplus*
