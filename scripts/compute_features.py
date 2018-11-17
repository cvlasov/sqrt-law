"""
This script runs JRM to compute the features of all JPEGs in a directory.
For each image, called "imageX.jpg" say, a file called "imageX.fea" is
generated. This file contains one line, which starts with the image's
filename followed by whitespace and then the whitespace-separated features.
"""

import argparse
import os
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("-I", "--input-dir", required=True,
                    help="Directory with all images")
args = parser.parse_args()

start = time.time()

for image_num in range(1,13350):
  image_partial_path = args.input_dir + 'image' + str(image_num).zfill(5)
  if os.path.isfile(image_partial_path + '.jpg'):
    subprocess.call('./jrm -a ' + image_partial_path + '.jpg'
                    + ' > ' + image_partial_path + '.fea', shell=True)

end = time.time()
print('\n------------------------\n')
print(str(end-start) + ' seconds elapsed')
