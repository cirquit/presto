#!/bin/bash

pythonscript="$1"

for threadcount in 1 2 4 8 1 2 4 8 1 2 4 8 1 2 4 8
do
  #                                 # sample count  #compression type  # storage  # dtype  # row-count (corresponds to datasize)
  python $pythonscript $threadcount 1500000         none               ceph-hdd   float32  1
  python $pythonscript $threadcount 750000          none               ceph-hdd   float32  2
  python $pythonscript $threadcount 375000          none               ceph-hdd   float32  4
  python $pythonscript $threadcount 187500          none               ceph-hdd   float32  8
  python $pythonscript $threadcount 93750           none               ceph-hdd   float32  16 
  python $pythonscript $threadcount 46875           none               ceph-hdd   float32  32
  python $pythonscript $threadcount 23437           none               ceph-hdd   float32  64
  python $pythonscript $threadcount 11718           none               ceph-hdd   float32  128
  python $pythonscript $threadcount 5859            none               ceph-hdd   float32  256
  python $pythonscript $threadcount 2929            none               ceph-hdd   float32  512
  python $pythonscript $threadcount 1464            none               ceph-hdd   float32  1024
  python $pythonscript $threadcount 732             none               ceph-hdd   float32  2048
 
  # uint's row-count is 4x compared to float32: 32bit / 8bit = 4x
  #                                 # sample count  #compression type  # storage  # dtype  # row-count (corresponds to datasize)
  python $pythonscript $threadcount 1500000         none               ceph-hdd   uint8  4
  python $pythonscript $threadcount 750000          none               ceph-hdd   uint8  8
  python $pythonscript $threadcount 375000          none               ceph-hdd   uint8  16
  python $pythonscript $threadcount 187500          none               ceph-hdd   uint8  32
  python $pythonscript $threadcount 93750           none               ceph-hdd   uint8  64 
  python $pythonscript $threadcount 46875           none               ceph-hdd   uint8  128
  python $pythonscript $threadcount 23437           none               ceph-hdd   uint8  256
  python $pythonscript $threadcount 11718           none               ceph-hdd   uint8  512
  python $pythonscript $threadcount 5859            none               ceph-hdd   uint8  1024
  python $pythonscript $threadcount 2929            none               ceph-hdd   uint8  2048
  python $pythonscript $threadcount 1464            none               ceph-hdd   uint8  4096
  python $pythonscript $threadcount 732             none               ceph-hdd   uint8  8192
done
