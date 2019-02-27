#!/bin/bash
size=$1
bits=$2

nohup ./run_txt_to_mat.sh /usr/local/matlab-r2014a/ features/size${size}_binary_${bits}b.fea features/size${size}_binary_${bits}b.mat &> size${size}_binary_${bits}b_mat.out &
