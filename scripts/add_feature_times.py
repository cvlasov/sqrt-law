"""
This script computes the total time elapsed during JRM feature computation
by summing the timing information output by the ten processes used in the
parallelized computation.

It is assumed that the files with the standard output from the ten processes
are called size{WIDTH}_binary_{BITS}b_fea_{X}.out, where X is the process number
in the range [0,9]. It is also assumed that the timing information in each of
these files is on the second-last line and that this line is of the form
"123.456s token1 token2" - for example "35.045 seconds elapsed".
"""

import argparse
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dir', default='./',
                    help='Relative path to directory with terminal output')
parser.add_argument('-w', '--width', required=True,
                    help='Image width, in pixels')
parser.add_argument('-b', '--bits', required=True,
                    help='Payload size, in bits')
args = parser.parse_args()

total = 0.0

for p in range(0,10):
  path = args.dir + 'size' + args.width + '_binary_' + args.bits + 'b_fea_' + \
         str(p) + '.out'
  ps = subprocess.Popen(('tail', '-1', path), stdout=subprocess.PIPE)
  line = ps.stdout.read()
  total += float(line.split()[0])

print('Total feature computation time for size ' + args.width + ' with ' + \
      args.bits + ' bits: ' + str(total) + 's')
