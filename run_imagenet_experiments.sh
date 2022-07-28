#!/bin/bash

pythonscript="imagenet_demo.py"

echo "---"
echo "I. Starting with short parallelism experiments...(~ 2h)"
echo "---"
# 1.1 Parallelism experiments + caching
for threadcount in 1 2 4 8
do
  echo 3 > /drop_caches
  compression="none"
  samplecount=8000
  runs=2
  pipelinemod="none"
  python -u $pythonscript $threadcount $compression $samplecount $runs $pipelinemod
done
# 1.2 clean up
rm -rf /tmp/imagenet*

echo "---"
echo "II. Caching experiments..."
echo "---"
# 2.1 Caching experiments
for threadcount in 8
do
  echo 3 > /drop_caches
  compression="none"
  samplecount=1281167
  runs=2
  pipelinemod="none"
  python -u $pythonscript $threadcount $compression $samplecount $runs $pipelinemod
done
# 2.2 Clean up
rm -rf /tmp/imagenet*

echo "---"
echo "III. Compression experiments..."
echo "---"
# 3.1 Compression experiments
for compression in ZLIB GZIP
do
  echo 3 > /drop_caches
  threadcount=8
  samplecount=1281167
  runs=1
  pipelinemod="none"
  python -u $pythonscript $threadcount $compression $samplecount $runs $pipelinemod
done
# 3.2 Clean up
rm -rf /tmp/imagenet*

echo "---"
echo "IV. Introducing new steps experiments..."
echo "---"
# 4.1 Greyscale before pixel-centering
echo 3 > /drop_caches
threadcount=8
compression="none"
samplecount=1281167
runs=1
pipelinemod="before-centering"
python -u $pythonscript $threadcount $compression $samplecount $runs $pipelinemod
# 4.2 Clean up
rm -rf /tmp/imagenet*

# 5.1 Greyscale after pixel-centering
echo 3 > /drop_caches
threadcount=8
compression="none"
samplecount=1281167
runs=1
pipelinemod="after-centering"
python -u $pythonscript $threadcount $compression $samplecount $runs $pipelinemod

# 5.2 Clean up
rm -rf /tmp/imagenet*
