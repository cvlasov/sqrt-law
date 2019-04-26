"""
This script converts all PGM files in a given input directory to JPEG, rotates
the portrait ones to landscape, identifies those that are large enough, crops
them to the given height and width, and places the resulting JPEGs in a given
output directory.

The original PGM files are assumed to be grayscale images.
"""

import argparse
import os
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--edge-crop', type=int, default=0,
                    help='Minimum number of pixels to crop from each edge')
parser.add_argument('-i', '--input-dir', default='original/',
                    help='Directory with all original PGM images')
parser.add_argument('-hei', '--cropped-height', type=int, default=1920,
                    help='Height in pixels to crop the images to')
parser.add_argument('-m', '--metadata', type=argparse.FileType('r'),
                    default='identify.txt', help='File with image metadata')
parser.add_argument('-o', '--output-dir', default='processed/',
                    help='Directory where processed images should be placed')
parser.add_argument('-q', '--quality-factor', type=int, default=80,
                    help='Quality factor to use for JPEG compression')
parser.add_argument('-w', '--cropped-width', type=int, default=2560,
                    help='Width in pixels to crop the images to')
args = parser.parse_args()

def handle_image(name, width, height):
  """
  Compress PGM image to JPEG, make it landscape (if it isn't already), check if
  it is large enough, crop to the specified dimensions, and place it in the
  output directory.
  """
  input_path = args.input_dir + name + '.pgm'
  temp_path = args.output_dir + name + '_temp.jpg'
  output_path = args.output_dir + name + '.jpg'

  # Check that file exists
  if not os.path.isfile(input_path):
    print('File {} does not exist. Skipping.'.format(input_path))
    return

  # Compress to JPEG
  subprocess.call('cjpeg -quality {:d} {} > {}'.format( \
                  args.quality_factor, input_path, output_path), shell=True)

  # Rotate the image to landscape, if necessary
  if width < height:
    subprocess.call('jpegtran -rotate 90 {} > {}'.format( \
                    output_path, temp_path), shell=True)
    temp = width
    width = height
    height = temp
  else:
    # Create a temporary file so that the next jpegtran call can use it
    subprocess.call('cp {} {}'.format(output_path, temp_path), shell=True)

  # Compute dimensions after trimming pixels outside outermost blocks
  width_after_trim = 8*int(width/8)
  height_after_trim = 8*int(height/8)

  # Check if the image is large enough to crop at least 32 pixels from each side
  crop = 32
  if width_after_trim - 2*crop >= args.cropped_width or \
     height_after_trim - 2*crop >= args.cropped_height:
    width_diff = width_after_trim - args.cropped_width
    height_diff = height_after_trim - args.cropped_height

    # Crop 32 pixels from each side (i.e. center crop)
    # The jpegtran -crop argument is of the form WxH+X+Y where W and H are the
    # width and height to crop to, respectively, and (X,Y) is the starting
    # point for cropping.
    crop_arg = '{:d}x{:d}+{:d}+{:d}'.format(args.cropped_width,  \
                                            args.cropped_height, \
                                            int(width_diff/2),   \
                                            int(height_diff/2))
    # -trim argument removes edge pixels that make image odd-sized
    subprocess.call('jpegtran -trim -crop {} {} > {}'.format( \
                    crop_arg, temp_path, output_path), shell=True)
  else:
    # Skip image
    print('{} is too small. Skipping.'.format(name))
    os.remove(output_path)

  # Remove the temporary file
  os.remove(temp_path)

  print('Done processing {}.'.format(name))

# --------------
# SCRIPT
start = time.time()

# Check that the input directory exists
if not os.path.isdir(args.input_dir):
  sys.exit('ERROR: Input directory {} does not exist.'.format(args.input_dir))

# Create output directory if it doesn't exist
if not os.path.isdir(args.output_dir):
  os.mkdir(args.output_dir)

# Process each image listed in the metadata file
for line in args.metadata.readlines():
  values = line.rstrip().split()
  dimensions = values[2].split('x')  # Format is '1234x5678'
  name = values[0][0:10]  # Extracts 'imageXXXX' from filename
  width = int(dimensions[0])
  height = int(dimensions[1])
  handle_image(name, width, height)

end = time.time()
print('\n------------------------')
print(str(end-start) + ' seconds elapsed')
