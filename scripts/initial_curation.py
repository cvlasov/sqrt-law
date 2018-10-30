"""
This script finds all JPEGs with specific dimensions in a specific
subdirectory, converts them to grayscale, rotates the portrait ones to
landscape, and puts all the resulting JPEGs into a specific subdirectory.
"""

import subprocess
import time

desired_width = 3072
desired_height = 2304

original_dir = 'original/'
dest_dir = 'size3072/'
metadata_file = 'metadata.txt'

def handle_image(name):
  """
  Convert image to grayscale, make it landscape (if it isn't already), and
  put it in the destination directory.
  """
  original_path = original_dir + name
  destination_path = dest_dir + name

  if width != desired_width:
    subprocess.call('jpegtran -rotate 90 -grayscale ' + original_path + \
                    ' > ' + destination_path, shell=True)
  else:
    subprocess.call('jpegtran -grayscale ' + original_path + ' > ' + \
                    destination_path, shell=True)

# SCRIPT
start = time.time()

with open(metadata_file, 'r') as metadata:
  # Start reading from the fourth line since the first three have other
  # information.
  for line in metadata.readlines()[3:]:
    values = line.rstrip().split()
    image_num = values[0]
    width = int(values[3])
    height = int(values[4])

    if (width == desired_width and height == desired_height) or \
       (width == desired_height and height == desired_width):
      name = 'image' + image_num.zfill(5) + '.jpg'
      handle_image(name)

end = time.time()
print(str(end-start) + ' seconds elapsed')
