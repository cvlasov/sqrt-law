#!/bin/bash
size=$1
bits=$2

nohup ./run_juniward_test.sh /usr/local/matlab-r2014a/ features/size${size}_cover.mat features/size${size}_binary_${bits}b.mat &> size${size}_binary_${bits}b_classifier.out &
