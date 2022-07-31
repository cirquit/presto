#!/bin/bash

pythonscript="openwebtext_modern_demo.py"

echo "Approximate runtime: h (I) + h (II) + h (III) = Xh"
echo "---"
echo "I. Starting with short parallelism experiments..."
echo "---"
# 1.1 Parallelism experiments + caching
for threadcount in 1 2 4 8
do
  echo 3 > /drop_caches
  compression="none"
  samplecount=8000
  runs=2
  python -u $pythonscript $threadcount $compression $samplecount $runs
done
# 1.2 clean up
rm -rf /tmp/owt*

echo "---"
echo "II. Caching experiments..."
echo "---"
# 2.1 Caching experiments
for threadcount in 8
do
  echo 3 > /drop_caches
  compression="none"
  samplecount=180662
  runs=2
  python -u $pythonscript $threadcount $compression $samplecount $runs
done
# 2.2 Clean up
rm -rf /tmp/owt*

echo "---"
echo "III. Compression experiments..."
echo "---"
# 3.1 Compression experiments
for compression in ZLIB GZIP
do
  echo 3 > /drop_caches
  threadcount=8
  samplecount=180662
  runs=1
  python -u $pythonscript $threadcount $compression $samplecount $runs
done
# 3.2 Clean up
rm -rf /tmp/owt*
