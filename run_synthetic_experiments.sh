#!/bin/bash

pythonscript="type_demo.py"

echo "---"
echo "I. Reading UINT8 from storage..."
echo "---"
echo 3 > /drop_caches
threadcount=8
runs=1
datatype="uint8"
pipeline_mod="read_experiment"
python -u $pythonscript $threadcount 732 $runs $datatype 8192 $pipeline_mod
# 1.2 clean up
rm -rf /tmp/synthetic*
