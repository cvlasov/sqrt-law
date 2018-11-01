"""
This script crops all JPEGs in a directory to the given dimensions and
puts all the cropped JPEGs into another directory. It crops 8x8 blocks
evenly from the top/bottom and left/right.
"""

import argparse
import os
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("-fr", "--from-dir", default='size3072/cover/',
                    help="Directory with all images")
parser.add_argument("-hei", "--height", type=int, required=True,
                    help="Height in pixels to crop the images to")
parser.add_argument("-to", "--to-dir", required=True,
                    help="Directory where images should be placed")
parser.add_argument("-wid", "--width", type=int, required=True,
                    help="Width in pixels to crop the images to")
args = parser.parse_args()

start = time.time()

original_width = 3072
original_height = 2304
width_diff = original_width - args.width
height_diff = original_height - args.height
vertical_blocks_to_crop = int(height_diff / 8)
horizontal_blocks_to_crop = int(width_diff / 8)

# The jpegtran -crop argument is of the form WxH+X+Y where W and H are the
# width and height to crop to, respectively, and (X,Y) is the starting
# point for cropping.
crop_args = str(args.width) + 'x' + str(args.height) + '+' \
            + str(8 * int(horizontal_blocks_to_crop / 2)) + '+' \
            + str(8 * int(vertical_blocks_to_crop / 2))

for image_name in os.listdir(args.from_dir):
  subprocess.call('jpegtran -perfect -crop ' + crop_args + ' ' + \
                  args.from_dir + image_name + ' > ' + args.to_dir + \
                  image_name, shell=True)

end = time.time()
print(str(end-start) + ' seconds elapsed')
