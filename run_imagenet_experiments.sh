#!/bin/bash

pythonscript="imagenet_demo.py"

echo "---"
echo "I. Starting with short parallelism experiments..."
echo "---"
# 1.1 Parallelism experiments + caching
for threadcount in 1 2 4 8
do
  compression="none"
  samplecount=8000
  runs=2
  python -u $pythonscript $threadcount $compression $samplecount $runs
done
# 1.2 clean up
rm -rf /tmp/imagenet*

echo "---"
echo "II. Caching experiments..."
echo "---"
# 2.1 Caching experiments
for threadcount in 8
do
  compression="none"
  samplecount=1281167
  runs=2
  python -u $pythonscript $threadcount $compression $samplecount $runs
done
# 2.2 Clean up
rm -rf /tmp/imagenet*

echo "---"
echo "III. Compression experiments..."
echo "---"
# 3.1 Compression experiments
for compression in ZLIB GZIP
do
  threadcount=8
  samplecount=1281167
  runs=1
  python -u $pythonscript $threadcount $compression $samplecount $runs
done
# 3.2 Clean up
rm -rf /tmp/imagenet*

echo "---"
echo "IV. Introducing new steps experiments..."
echo "---"
# 4.1 Greyscale before pixel-centering
threadcount=8
samplecount=1281167
runs=1
python -u imagenet_before_pixel_centering_demo.py $threadcount $compression $samplecount $runs
# 4.2 Clean up
rm -rf /tmp/imagenet*

# 5.1 Greyscale after pixel-centering
threadcount=8
samplecount=1281167
runs=1
python -u imagenet_after_pixel_centering_demo.py $threadcount $compression $samplecount $runs

# 5.2 Clean up
rm -rf /tmp/imagenet*
