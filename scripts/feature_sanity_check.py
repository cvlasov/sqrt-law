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

min_sum = -1
max_sum = -1

for filename in os.listdir(args.input_dir):
  name, extension = os.path.splitext(filename)
  if extension == '.fea':
    feature_sum = compute_sum(args.input_dir + filename)
    if min_sum == -1 and max_sum == -1:  # first feature
      min_sum = feature_sum
      max_sum = feature_sum
    else:
      min_sum = min(min_sum, feature_sum)
      max_sum = max(max_sum, feature_sum)

end = time.time()

print('Minimum feature sum: ' + str(min_sum))
print('Maximum feature sum: ' + str(max_sum))
print('------------------------')
print(str(end-start) + ' seconds elapsed')
