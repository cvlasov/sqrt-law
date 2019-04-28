"""
This script crops all JPEGs in a directory to the given dimensions and
puts all the cropped JPEGs into another directory. It crops 8x8 blocks
evenly from the top/bottom and left/right.

Both image dimensions are expected to be multiples of 8 pixels. If not,
jpegtran's "-perfect" switch fails with an error.
"""

import argparse
import os
import subprocess
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-dir', required=True,
                    help='Directory with all images')
parser.add_argument('-hei', '--new-height', type=int, required=True,
                    help='Height in pixels to crop the images to')
parser.add_argument('-o', '--output-dir', required=True,
                    help='Directory where cropped images should be placed')
parser.add_argument('-oh', '--original-height', type=int, required=True,
                    help='Current height in pixels of the images')
parser.add_argument('-ow', '--original-width', type=int, required=True,
                    help='Current width in pixels of the images')
parser.add_argument('-wid', '--new-width', type=int, required=True,
                    help='Width in pixels to crop the images to')
args = parser.parse_args()

# Check that the input directory exists
if not os.path.isdir(args.input_dir):
  sys.exit('ERROR: Input directory {} does not exist.'.format(args.input_dir))

# Create output directory if it doesn't exist
if not os.path.isdir(args.output_dir):
  os.makedirs(args.output_dir)

start = time.time()

width_diff = args.original_width - args.new_width
height_diff = args.original_height - args.new_height
vertical_blocks_to_crop = int(height_diff / 8)
horizontal_blocks_to_crop = int(width_diff / 8)

# The jpegtran -crop argument is of the form WxH+X+Y where W and H are the
# width and height to crop to, respectively, and (X,Y) is the starting
# point for cropping.
crop_args = '{:d}x{:d}+{:d}+{:d}'.format(args.new_width, args.new_height,
            8 * int(horizontal_blocks_to_crop / 2),
            8 * int(vertical_blocks_to_crop / 2))

for image_name in os.listdir(args.input_dir):
  subprocess.call('jpegtran -perfect -crop {} {} > {}'.format(crop_args,
                  args.input_dir + image_name, args.output_dir + image_name),
                  shell=True)

end = time.time()
print('\n------------------------')
print(str(end-start) + ' seconds elapsed')
