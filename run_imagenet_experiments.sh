#!/bin/bash

pythonscript="imagenet_demo.py"

echo "IV. Introducing new steps experiments..."
echo "---"
# 4.1 Greyscale before pixel-centering
echo 3 > /drop_caches
threadcount=8
compression="none"
#samplecount=1281167
samplecount=8000
runs=1
pipelinemod="before-centering"
python -u $pythonscript $threadcount $compression $samplecount $runs $pipelinemod
# 4.2 Clean up
rm -rf /tmp/imagenet*

# 5.1 Greyscale after pixel-centering
echo 3 > /drop_caches
threadcount=8
compression="none"
#samplecount=1281167
samplecount=8000
runs=1
pipelinemod="after-centering"
python -u $pythonscript $threadcount $compression $samplecount $runs $pipelinemod

# 5.2 Clean up
rm -rf /tmp/imagenet*
