"""
This script creates a single file with the features of all images in a
directory, where each line is whitespace-separated and has the image name
followed by the features (in row order), separated by whitespace. This file
uses the precomputed features, which are stored in existing text files, with
one file per image in the format "imageXXXXX.fea".
"""

import argparse
import os
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("-I", "--input-dir", required=True,
                    help="Directory with the feature files of all images")
parser.add_argument("-O", "--output-file", required=True,
                    help="Path and name of generated file with all features")
args = parser.parse_args()

start = time.time()
subprocess.call('touch ' + args.output_file, shell=True)

with open(args.output_file, "a") as combined_feature_file:
  for image_num in range(1,13350):
    image_fea_path = args.input_dir + 'image' + str(image_num).zfill(5) + '.fea'
    if os.path.isfile(image_fea_path):
      with open(image_fea_path) as feature_file:
        # Each file has a single line.
        tokens = feature_file.readline().strip().split()
        # The first token on each line is the image path. We want this to be
        # just the image name so that cover and stego image names can be
        # compared. Without this, the paths would never match since the cover
        # and stego images are in different directories.
        tokens[0] = os.path.basename(tokens[0])
        combined_feature_file.write(" ".join(tokens) + "\n")

end = time.time()
print('\n------------------------')
print(str(end-start) + ' seconds elapsed\n')
