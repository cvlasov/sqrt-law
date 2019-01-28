"""
This script creates a file with one line per image size. Each line has the
height, width, and total number of pixels followed by the number of bits that
should be embedded in the experiments. These numbers are O(1), O(sqrt(n)),
O(sqrt(n)*log(n)), and O(n) in the total number n of pixels in each image size.

The file is formatted so that the contents can be copy-pasted into a LaTeX
file inside a "tabular" environment.

Only works with Python3 due to the second parameter to the log function.
"""

import argparse
import subprocess
import time

from math import log,sqrt

sizes = [(3072,2304), (2912,2184), (2720,2040), (2528,1896), (2304,1728),
         (2048, 1536), (1792,1344), (1472,1104), (1056,792), (320,240)]

# J-UNIWARD with alpha=0.3 on 1056x792 produced a MinPE value of around 0.22
# so those results are used to compute the numbers of bits to embed in the
# real project experiments.
nz_coef = 120746          # Average number of non-zero coefficients per
                          # 1056x792 image
alpha = 0.3               # Bits per non-zero coefficient that were embedded
n_1056 = 1056 * 792       # Number of pixels in each 1056x792 image
m_1056 = alpha * nz_coef  # Average number of bits embedded per image

n_mid = 2048 * 1536                    # Number of pixels per middle-size image
m_mid = m_1056 * sqrt(n_mid / n_1056)  # Number of bits to embed per middle-size
                                       # image, assuming the square root law
                                       # holds

# Constants used for computing the specific numbers of bits to embed, which are
# O(1), O(sqrt(n)), O(sqrt(n)*log(n)), and O(n), respectively, where n is the
# number of pixels.
r1 = m_mid
r2 = m_mid / sqrt(n_mid)
r3 = m_mid / (sqrt(n_mid) * log(n_mid))
r4 = m_mid / n_mid

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output-file', required=True,
                    type=argparse.FileType('w'),
                    help='Path and name of generated file with payload sizes')
args = parser.parse_args()

start = time.time()

for (w,h) in sizes:
  n = w * h  # Number of pixels
  values = [w, h, n, r1, r2*sqrt(n), r3*sqrt(n)*log(n,2), r4*n]
  values = map(lambda x: str(int(x)), values)
  args.output_file.write(' & '.join(values) + ' \\\\\n')

end = time.time()

args.output_file.write('\n')
args.output_file.write('r1 = ' + str(r1) + '\n')
args.output_file.write('r2 = ' + str(r2) + '\n')
args.output_file.write('r3 = ' + str(r3) + '\n')
args.output_file.write('r4 = ' + str(r4) + '\n')
print('\n------------------------')
print(str(end-start) + ' seconds elapsed\n')
