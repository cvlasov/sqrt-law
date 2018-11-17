"""
This script computes the sum of the features for each JPEGs in a directory
and prints the minimum and maximum feature sums.
"""

import argparse
import os
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("-I", "--input-dir", help="Directory with all images")
args = parser.parse_args()

def compute_sum(filename):
  sum = 0.0
  with open(filename, 'r') as f:
    for line in f:  # only one line
      for feature in line.split()[1:]:
        sum += float(feature)
  return sum


# SCRIPT
start = time.time()

zero_sum_count = 0
expected_sum_count = 0
images_with_zero_sum = ''

for filename in os.listdir(args.input_dir):
  name, extension = os.path.splitext(filename)
  if extension == '.fea':
    feature_sum = compute_sum(args.input_dir + filename)
    if feature_sum == 0:
      zero_sum_count += 1
      images_with_zero_sum += filename + '\n'
    elif 1345.9 < feature_sum and feature_sum < 1346.1:
      expected_sum_count += 1

end = time.time()

format_str = '%12s | %8s'
print(format_str % ('Feature sum', '# images'))
print('------------------------')
print(format_str % (0, zero_sum_count))
print(format_str % (1346, expected_sum_count))
print('------------------------')
print(format_str % ('', (zero_sum_count + expected_sum_count)))
print('------------------------')
print(str(end-start) + ' seconds elapsed')
print('------------------------')
print('Images with feature sum = 0:\n' + images_with_zero_sum)
