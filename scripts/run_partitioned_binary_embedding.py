"""
This script runs binary J-UNIWARD embedding on all cover images of a particular
size. It splits the cover images into ten groups (given by their image numbers,
mod 10) and starts ten processes, one per group.

It is suspected that there is a memory leak in the J-UNIWARD code, so starting
ten processes that each process around a tenth of the original number of cover
images means that each process releases its memory after a tenth of the time,
which reduces the chances of a memory leak causing the server to start using
swap memory and significantly slowing down progress.
"""

import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--size", required=True,
                    help="Image size (i.e. # of pixels on longest dimension)")
parser.add_argument("-b", "--bits", required=True,
                    help="Number of payload bits")
args = parser.parse_args()

for digit in range(0,10):
  size = str(args.size)
  bits = str(args.bits)
  d = str(digit)
  subprocess.call('nohup ./BINARY-EMBED -v -I size' + size + '/cover/ ' +
                  '-O size' + size + '/stego-' + bits + 'b/ -b ' + bits +
                  ' --partition -d ' + d + ' &> size' + size + '_binary_' +
                  bits + 'b_rest_' + d + '.out &', shell=True)
