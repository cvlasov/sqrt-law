"""
This script runs JRM to compute the features of all JPEGs in a directory.
For each image, called "imageX.jpg" say, a file called "imageX.fea" is
generated. This file contains one line, which starts with the image's
filename followed by whitespace and then the whitespace-separates features.
"""

import argparse
import os
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("-I", "--input-dir", help="Directory with all images")
args = parser.parse_args()

start = time.time()

for image_name in os.listdir(args.input_dir):
  filename, file_ext = os.path.splitext(image_name)
  if file_ext == '.jpg':
    subprocess.call('./jrm -a ' + args.input_dir + image_name + ' > '
                    + args.input_dir + filename + '.fea', shell=True)

end = time.time()
print('\n------------------------\n')
print(str(end-start) + ' seconds elapsed')
