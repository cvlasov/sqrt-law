#!/bin/bash
size=$1
bits=$2

nohup python compute_features.py -I size${size}/stego-${bits}b/ &> size${size}_binary_${bits}b_fea.out &
