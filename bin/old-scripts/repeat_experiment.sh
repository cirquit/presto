#!/bin/bash

pythonscript="$1"

for threadcount in 8 8 8 8 8
do
  # adapt this to be compatible with the corresponding datasets
  for samplecount in 28539
  do
    # comment out the compression configuration you do not need
    for compression in none ZLIB GZIP
    do
      # same thing for the storage
      for storagetype in ceph-hdd #local-vm-ssd
      do
        python $pythonscript $threadcount $samplecount $compression $storagetype
      done
    done
  done 
done
