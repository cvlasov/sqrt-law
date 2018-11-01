"""
This script finds all JPEGs with specific dimensions in a directory,
converts them to grayscale, rotates the portrait ones to landscape, and
puts all the resulting JPEGs into another directory.
"""

import argparse
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("-fr", "--from-dir", default='original/',
                    help="Directory with all images")
parser.add_argument("-hei", "--height", type=int, default=2304,
                    help="Height in pixels of the images to select")
parser.add_argument("-m", "--metadata", type=argparse.FileType('r'),
                    default='metadata.txt',
                    help="File with metadata about the images")
parser.add_argument("-to", "--to-dir", default='size3072/',
                    help="Directory where images should be placed")
parser.add_argument("-wid", "--width", type=int, default=3072,
                    help="Width in pixels of the images to select")
args = parser.parse_args()

def handle_image(name):
  """
  Convert image to grayscale, make it landscape (if it isn't already), and
  put it in the destination directory.
  """
  from_path = args.from_dir + name
  to_path = args.to_dir + name

  if width != args.width:
    subprocess.call('jpegtran -rotate 90 -grayscale ' + from_path + ' > ' \
                    + to_path, shell=True)
  else:
    subprocess.call('jpegtran -grayscale ' + from_path + ' > ' + to_path,\
                    shell=True)

# SCRIPT
start = time.time()

# Start reading from the fourth line since the first three have other
# information.
for line in args.metadata.readlines()[3:]:
  values = line.rstrip().split()
  image_num = values[0]
  width = int(values[3])
  height = int(values[4])

  if (width == args.width and height == args.height) or \
     (width == args.height and height == args.width):
    name = 'image' + image_num.zfill(5) + '.jpg'
    handle_image(name)

end = time.time()
print(str(end-start) + ' seconds elapsed')
