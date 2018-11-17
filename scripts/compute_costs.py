"""
This script runs the hacked J-UNIWARD to compute the costs of all JPEGs in a
directory. For each image, called "imageX.jpg" say, a file called "imageX.costs"
is generated. This file contains one cost per line, with costs written in a
row-by-row fashion.
"""

import argparse
import os
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("-I", "--input-dir", help="Directory with all images")
parser.add_argument("-O", "--output-dir",
                    help="Directory to save feature files")
args = parser.parse_args()

start = time.time()

for image_num in range(1,13350):
  image_partial_path = args.input_dir + 'image' + str(image_num).zfill(5)
  if os.path.isfile(image_partial_path + '.jpg'):
    subprocess.call('./J-UNIWARD -v -i ' + image_partial_path + '.jpg'
                    + ' -O ' + args.output_dir + ' -a 0.4', shell=True)

end = time.time()
print('\n------------------------\n')
print(str(end-start) + ' seconds elapsed')
