#!/bin/bash
size=$1
bits=$2

mkdir size${size}/stego-${bits}b/

for i in {0..9}
do
  nohup ./BINARY-EMBED -v -I size${size}/cover/ -O size${size}/stego-${bits}b/ -b ${bits} --partition -d ${i} &> size${size}_binary_${bits}b_${i}.out &
done
