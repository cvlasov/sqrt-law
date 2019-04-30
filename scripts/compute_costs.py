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
  for n in range(0,int(13349/num_processes)+1):
    image_num = n * num_processes + process_id
    image_path = args.input_dir + 'image' + str(image_num).zfill(5) + '.jpg'
    cost_path = args.output_dir + 'image' + str(image_num).zfill(5) + '.costs'
    if os.path.isfile(image_path) and not os.path.isfile(cost_path):
      # No -v because printing gets messed up with multiple processes running
      subprocess.call('./J-UNIWARD-COSTS -i ' + image_path + ' -O ' + \
                      args.output_dir + ' -a 0.4', shell=True)

parser = argparse.ArgumentParser()
parser.add_argument('-I', '--input-dir', required=True,
                    help='Directory with all images')
parser.add_argument('-O', '--output-dir', required=True,
                    help='Directory to save cost files')
args = parser.parse_args()

start = time.time()
p = Pool(num_processes)
p.map(run, range(0,num_processes))
p.close()
p.join()
end = time.time()
print('\n------------------------')
print(str(end-start) + ' seconds elapsed\n')
