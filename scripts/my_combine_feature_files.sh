#!/bin/bash
size=$1
bits=$2

nohup python combine_feature_files.py -I size${size}/stego-${bits}b/ -O features/size${size}_binary_${bits}b.fea &> size${size}_binary_${bits}b_combine_features.out &
