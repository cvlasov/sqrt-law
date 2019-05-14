import argparse
import matplotlib.pyplot as plt
import os

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bits', type=int, required=True,
                    help='Payload size, in bits')
parser.add_argument('-s', '--size', type=int, required=True,
                    help='Image width, in pixels')
parser.add_argument('-f', '--file', type=argparse.FileType('r'), required=True,
                    help='File with ROC curve points')
args = parser.parse_args()

lines = args.file.readlines()
x = []
y = []
min_pe_index = int(lines[-1])

# Loop through all except the last line (which contains minPE index)
for line in lines[:-1]:
  values = line.rstrip().split()
  x.append(float(values[0]))
  y.append(float(values[1]))

# Create plot
plt.figure(figsize=(12,10))
x_label = 'PFA'
y_label = '1-PMD'
plt.plot(x, y, 'k')
plt.plot(x[min_pe_index], y[min_pe_index], 'ro', label='MinPE')
plt.xlabel(r'$P_{FA}$')
plt.ylabel(r'$1-P_{MD}$')
plt.title('ROC curve (size {:d}, {:d} bits)'.format(args.size, args.bits))
plt.legend()

# Save plot
plt.savefig('size{:d}_{:d}b_roc.png'.format(args.size, args.bits))
