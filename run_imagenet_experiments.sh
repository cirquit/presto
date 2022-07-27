#!/bin/bash

pythonscript="imagenet_demo.py"

for threadcount in 8
do
  # comment out the compression configuration you do not need
  for compression in none #ZLIB GZIP
  do
    python -u $pythonscript $threadcount $compression 
  done
done

rm -rf /tmp/imagenet*
