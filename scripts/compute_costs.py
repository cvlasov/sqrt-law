"""
This script runs the hacked J-UNIWARD to compute the costs of all JPEGs in a
directory. For each image, called "imageX.jpg" say, a file called "imageX.costs"
is generated. This file contains one cost per line, with costs written in a
row-by-row fashion.
"""

import argparse
from multiprocessing import Pool
import os
import subprocess
import time

num_processes = 10

def run(process_id):
  for n in range(0,int(13350/num_processes)):
    image_num = n * num_processes + process_id
    image_partial_path = args.input_dir + 'image' + str(image_num).zfill(5)
    if os.path.isfile(image_partial_path + '.jpg'):
      subprocess.call('./J-UNIWARD -v -i ' + image_partial_path + '.jpg'
                      + ' -O ' + args.output_dir + ' -a 0.4', shell=True)

parser = argparse.ArgumentParser()
parser.add_argument("-I", "--input-dir", required=True,
                    help="Directory with all images")
parser.add_argument("-O", "--output-dir", required=True,
                    help="Directory to save cost files")
args = parser.parse_args()

start = time.time()
p = Pool(num_processes)
p.map(run, range(0,num_processes))
p.close()
p.join()
end = time.time()
print('\n------------------------\n')
print(str(end-start) + ' seconds elapsed')
