import argparse
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bits', type=int, required=True,
                    help='Payload size, in bits')
parser.add_argument('-s', '--size', type=int, required=True,
                    help='Image width, in pixels')
args = parser.parse_args()

x = []
y = []
min_pe_index = -1

roc_points_filename = \
    'roc/points/size{:d}_{:d}b_roc.txt'.format(args.size, args.bits)
with open(roc_points_filename, 'r') as roc_points_file:
    lines = roc_points_file.readlines()
    min_pe_index = int(lines[-1]) - 1

    # Loop through all except the last line (which contains minPE index)
    for line in lines[:-1]:
      values = line.rstrip().split()
      x.append(float(values[0]))
      y.append(float(values[1]))

# Create plot
plt.figure(figsize=(7,7))
plt.xlabel(r'$f_p$')
plt.ylabel(r'$1-f_n$')

# Plot ROC curve
plt.plot(x, y, color='r')

# Identify MinPE point
plt.plot(x[min_pe_index], y[min_pe_index], color='k', marker='o', markersize=8)

# Plot ROC curve of a random classifier for reference
plt.plot([0.0,1.0], [0.0,1.0], color='#696969', linestyle='dashed')

# Save plot
plt.savefig('roc/curves/size{:d}_{:d}b_roc.png'.format(args.size, args.bits))
