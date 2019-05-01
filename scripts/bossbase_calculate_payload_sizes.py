"""
This script creates a file with one line per image size. Each line has the
height, width, and total number of pixels followed by the number of bits that
should be embedded in the experiments. These numbers are O(1), O(sqrt(n)),
O(sqrt(n)*log(n)), and O(n) in the total number n of pixels in each image size.

The file is formatted so that the contents can be copy-pasted into a LaTeX
file inside a "tabular" environment.

Only works with Python3 due to the second parameter to the log function, which
indicates the base of the logarithm and was introduced in Python3.
"""

import argparse
import subprocess
import time

from math import log,sqrt

sizes = [(896,672), (1280,960), (1536,1152), (1792,1344), (2016,1512),
         (2172,1632), (2368,1776), (2560,1920)]

# Binary J-UNIWARD embedding with a payload of 41287 bits in 1792x1344 images
# produced a MinPE value of around 0.2028 so those results are used to compute
# the numbers of bits to embed in the real experiments.
n_1792 = 1792 * 1344      # Number of pixels in each 1792x1344 image
m_1792 = 41287            # Number of bits embedded per image

n_mid = n_1792            # Number of pixels per middle-size image
m_mid = m_1792            # Number of bits to embed per middle-size image

# Constants used for computing the specific numbers of bits to embed, which are
# O(1), O(sqrt(n)), O(sqrt(n)*log(n)), and O(n), respectively, where n is the
# number of pixels.
r1 = m_mid
r2 = m_mid / sqrt(n_mid)
r3 = m_mid / (sqrt(n_mid) * log(n_mid,2))
r4 = m_mid / n_mid

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output-file', required=True,
                    type=argparse.FileType('w'),
                    help='Path and name of generated file with payload sizes')
args = parser.parse_args()

start = time.time()
coefficients = [0.7, 1.0, 1.3]

for c in coefficients:
  args.output_file.write('PAYLOADS * {}\n'.format(c))
  args.output_file.write('\\begin{tabular}{ r r r | r r r r }\n')
  args.output_file.write('Width & Height & Pixels & $O(1)$ & $O(\sqrt{n})$ & $O(\sqrt{n} \cdot \log n)$ & $O(n)$ \\\\ \hline\n')
  for (w,h) in sizes:
    n = w * h  # Number of pixels
    values = [w, h, n, c*r1, c*r2*sqrt(n), c*r3*sqrt(n)*log(n,2), c*r4*n]
    values = map(lambda x: str(int(x)), values)
    args.output_file.write(' & '.join(values) + ' \\\\\n')
  args.output_file.write('\end{tabular}\n\n')

end = time.time()

args.output_file.write('CONSTANTS\n')
args.output_file.write('\\begin{tabular}{ r | r r r }\n')
args.output_file.write('& $-30\%$ & Original & $+30\%$ \\\\ \\hline\n')
args.output_file.write('r1 & {} & {} & {} \\\\\n'.format(r1*0.7, r1, r1*1.3))
args.output_file.write('r2 & {} & {} & {} \\\\\n'.format(r2*0.7, r2, r2*1.3))
args.output_file.write('r3 & {} & {} & {} \\\\\n'.format(r3*0.7, r3, r3*1.3))
args.output_file.write('r4 & {} & {} & {} \\\\\n'.format(r4*0.7, r4, r4*1.3))
args.output_file.write('\end{tabular}\n\n')

print('\n------------------------')
print(str(end-start) + ' seconds elapsed\n')
