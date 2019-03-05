"""
This script computes the total time elapsed during binary J-UNIWARD embedding
by summing the timing information output by the ten processes used in the
parallelized computation.

It is assumed that the files with the standard output from the ten processes
are called size{WIDTH}_binary_{BITS}b_{X}.out, where X is the process number
in the range [0,9]. It is also assumed that the timing information in each of
these files is on the second-last line and that this line is of the form
"token1 token2 123.456s" - for example "Time elapsed: 35.045s".
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
  path = args.dir + 'size' + args.width + '_binary_' + args.bits + 'b_' + \
         str(p) + '.out'
  ps = subprocess.Popen(('tail', '-2', path), stdout=subprocess.PIPE)
  line = subprocess.check_output(('head', '-1'), stdin=ps.stdout)
  ps.wait()
  total += float(line.split()[2][:-1])

print('Total embedding time for size ' + args.width + ' with ' + args.bits + \
      ' bits: ' + str(total) + 's')
