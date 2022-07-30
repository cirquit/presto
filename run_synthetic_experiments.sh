#!/bin/bash

pythonscript="synthetic_demo.py"

echo "Approximate runtime: 1h (I) + 1h (II) + (III) + (IV) + 8h (V) + (VI)= 10h"
echo "---"
echo "I. Reading UINT8 from storage..."
echo "---"
echo 3 > /drop_caches
threadcount=8
runs=1
datatype="uint8"
pipeline_mod="read-experiment"
python -u $pythonscript $threadcount 732    $runs $datatype 8192 $pipeline_mod
python -u $pythonscript $threadcount 1463   $runs $datatype 4096 $pipeline_mod
python -u $pythonscript $threadcount 2929   $runs $datatype 2048 $pipeline_mod
python -u $pythonscript $threadcount 5859   $runs $datatype 1024 $pipeline_mod
python -u $pythonscript $threadcount 11718  $runs $datatype 512  $pipeline_mod
python -u $pythonscript $threadcount 23437  $runs $datatype 256  $pipeline_mod
python -u $pythonscript $threadcount 46875  $runs $datatype 128  $pipeline_mod
python -u $pythonscript $threadcount 93750  $runs $datatype 64   $pipeline_mod
python -u $pythonscript $threadcount 187500 $runs $datatype 32   $pipeline_mod
python -u $pythonscript $threadcount 375000 $runs $datatype 16   $pipeline_mod
python -u $pythonscript $threadcount 750000 $runs $datatype 8    $pipeline_mod
python -u $pythonscript $threadcount 1500000 $runs $datatype 4    $pipeline_mod
# 1.2 clean up
rm -rf /tmp/synthetic*

echo "II. Reading FLOAT32 from storage..."
echo "---"
threadcount=8
runs=1
datatype="float32"
pipeline_mod="read-experiment"
echo 3 > /drop_caches
python -u $pythonscript $threadcount 732    $runs $datatype 2048 $pipeline_mod
python -u $pythonscript $threadcount 1463   $runs $datatype 1024 $pipeline_mod
python -u $pythonscript $threadcount 2929   $runs $datatype 512  $pipeline_mod
python -u $pythonscript $threadcount 5859   $runs $datatype 256  $pipeline_mod
python -u $pythonscript $threadcount 11718  $runs $datatype 128  $pipeline_mod
python -u $pythonscript $threadcount 23437  $runs $datatype 64   $pipeline_mod
python -u $pythonscript $threadcount 46875  $runs $datatype 32   $pipeline_mod
python -u $pythonscript $threadcount 93750  $runs $datatype 16   $pipeline_mod
python -u $pythonscript $threadcount 187500 $runs $datatype 8    $pipeline_mod
python -u $pythonscript $threadcount 375000 $runs $datatype 4    $pipeline_mod
python -u $pythonscript $threadcount 750000 $runs $datatype 2    $pipeline_mod
python -u $pythonscript $threadcount 1500000 $runs $datatype 1    $pipeline_mod
# 2.2 clean up
rm -rf /tmp/synthetic*

echo "III. Reading FLOAT32 from storage with system-caching enabled..."
echo "---"
echo 3 > /drop_caches
threadcount=8
runs=2
datatype="float32"
pipeline_mod="sys-caching-read"
python -u $pythonscript $threadcount 732    $runs $datatype 2048 $pipeline_mod
python -u $pythonscript $threadcount 1463   $runs $datatype 1024 $pipeline_mod
python -u $pythonscript $threadcount 2929   $runs $datatype 512  $pipeline_mod
python -u $pythonscript $threadcount 5859   $runs $datatype 256  $pipeline_mod
python -u $pythonscript $threadcount 11718  $runs $datatype 128  $pipeline_mod
python -u $pythonscript $threadcount 23437  $runs $datatype 64   $pipeline_mod
python -u $pythonscript $threadcount 46875  $runs $datatype 32   $pipeline_mod
python -u $pythonscript $threadcount 93750  $runs $datatype 16   $pipeline_mod
python -u $pythonscript $threadcount 187500 $runs $datatype 8    $pipeline_mod
python -u $pythonscript $threadcount 375000 $runs $datatype 4    $pipeline_mod
python -u $pythonscript $threadcount 750000 $runs $datatype 2    $pipeline_mod
python -u $pythonscript $threadcount 1500000 $runs $datatype 1    $pipeline_mod
# 3.2 clean up
rm -rf /tmp/synthetic*

echo "IV. Reading FLOAT32 from storage with application-caching enabled..."
echo "---"
echo 3 > /drop_caches
threadcount=8
runs=2
datatype="float32"
pipeline_mod="app-caching-read"
python -u $pythonscript $threadcount 732    $runs $datatype 2048 $pipeline_mod
python -u $pythonscript $threadcount 1463   $runs $datatype 1024 $pipeline_mod
python -u $pythonscript $threadcount 2929   $runs $datatype 512  $pipeline_mod
python -u $pythonscript $threadcount 5859   $runs $datatype 256  $pipeline_mod
python -u $pythonscript $threadcount 11718  $runs $datatype 128  $pipeline_mod
python -u $pythonscript $threadcount 23437  $runs $datatype 64   $pipeline_mod
python -u $pythonscript $threadcount 46875  $runs $datatype 32   $pipeline_mod
python -u $pythonscript $threadcount 93750  $runs $datatype 16   $pipeline_mod
python -u $pythonscript $threadcount 187500 $runs $datatype 8    $pipeline_mod
python -u $pythonscript $threadcount 375000 $runs $datatype 4    $pipeline_mod
python -u $pythonscript $threadcount 750000 $runs $datatype 2    $pipeline_mod
python -u $pythonscript $threadcount 1500000 $runs $datatype 1    $pipeline_mod
# 4.2 clean up
rm -rf /tmp/synthetic*

echo "V. Reading FLOAT32 from storage - Multithreaded..."
echo "---"
echo 3 > /drop_caches
for threadcount in 1 2 4 8
do
  runs=1
  datatype="float32"
  pipeline_mod="parallelism"
  python -u $pythonscript $threadcount 732    $runs $datatype 2048 $pipeline_mod
  python -u $pythonscript $threadcount 1463   $runs $datatype 1024 $pipeline_mod
  python -u $pythonscript $threadcount 2929   $runs $datatype 512  $pipeline_mod
  python -u $pythonscript $threadcount 5859   $runs $datatype 256  $pipeline_mod
  python -u $pythonscript $threadcount 11718  $runs $datatype 128  $pipeline_mod
  python -u $pythonscript $threadcount 23437  $runs $datatype 64   $pipeline_mod
  python -u $pythonscript $threadcount 46875  $runs $datatype 32   $pipeline_mod
  python -u $pythonscript $threadcount 93750  $runs $datatype 16   $pipeline_mod
  python -u $pythonscript $threadcount 187500 $runs $datatype 8    $pipeline_mod
  python -u $pythonscript $threadcount 375000 $runs $datatype 4    $pipeline_mod
  python -u $pythonscript $threadcount 750000 $runs $datatype 2    $pipeline_mod
  python -u $pythonscript $threadcount 1500000 $runs $datatype 1    $pipeline_mod
done
# 5.2 clean up
rm -rf /tmp/synthetic*

echo "VI. RMS processing runs..."
echo "---"
echo 3 > /drop_caches
for threadcount in 1 2 4 8
do
  for pipeline_mod in tf-computation np-computation
  do
  threadcount=8
  runs=1
  datatype="float32"
  python -u $pythonscript $threadcount 732    $runs $datatype 2048 $pipeline_mod
  python -u $pythonscript $threadcount 1463   $runs $datatype 1024 $pipeline_mod
  python -u $pythonscript $threadcount 2929   $runs $datatype 512  $pipeline_mod
  python -u $pythonscript $threadcount 5859   $runs $datatype 256  $pipeline_mod
  python -u $pythonscript $threadcount 11718  $runs $datatype 128  $pipeline_mod
  python -u $pythonscript $threadcount 23437  $runs $datatype 64   $pipeline_mod
  python -u $pythonscript $threadcount 46875  $runs $datatype 32   $pipeline_mod
  python -u $pythonscript $threadcount 93750  $runs $datatype 16   $pipeline_mod
  python -u $pythonscript $threadcount 187500 $runs $datatype 8    $pipeline_mod
  python -u $pythonscript $threadcount 375000 $runs $datatype 4    $pipeline_mod
  python -u $pythonscript $threadcount 750000 $runs $datatype 2    $pipeline_mod
  python -u $pythonscript $threadcount 1500000 $runs $datatype 1    $pipeline_mod
  done
done
# 6.2 clean up
rm -rf /tmp/synthetic*

