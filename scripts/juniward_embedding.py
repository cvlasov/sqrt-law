"""
This script runs the original J-UNIWARD to simulate the embedding of 0.4 bits
per non-zero AC DCT coefficient in each of the JPEGs in the input directory.
For each image "input-dir/imageX.jpg", a new image "output-dir/imageX.jpg" is
created.
"""

import argparse
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("-I", "--input-dir", required=True,
                    help="Directory with all images")
parser.add_argument("-O", "--output-dir", required=True,
                    help="Directory to save stego images")
args = parser.parse_args()

start = time.time()
subprocess.call('./J-UNIWARD -v -I ' + args.input_dir
                + ' -O ' + args.output_dir + ' -a 0.4', shell=True)
end = time.time()
print('\n------------------------\n')
print(str(end-start) + ' seconds elapsed')
