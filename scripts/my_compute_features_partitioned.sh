#!/bin/bash
size=$1
bits=$2

for i in {0..9}
do
  nohup python compute_features.py -I size${size}/stego-${bits}b/ -d ${i} &> size${size}_binary_${bits}b_fea_${i}.out &
done

