"""
This script runs the hacked J-UNIWARD to compute the costs of all JPEGs in a
directory. For each image, called "imageX.jpg" say, a file called "imageX.costs"
is generated. This file contains one cost per line, with costs written in a
row-by-row fashion.
"""

import argparse
import os
import subprocess
import threading
import time

num_threads = 10

def run(self):
  for n in range(0,int(13350/num_threads)):
    image_num = n * num_threads + thread_id
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

for thread_id in range(0,num_threads):
  thread = threading.Thread(target=run, args=(thread_id, ))
  thread.start()
  thread.join()

end = time.time()
print('\n------------------------\n')
print(str(end-start) + ' seconds elapsed')
