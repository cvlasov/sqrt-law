import argparse
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--rate', type=int, required=True,
                    help='Payload rate (1=constant, 2=sqrt, 3=sqrt*log, 4=linear)')
parser.add_argument("-t", "--with-title", action='store_true',
                    help="Include graph title")
args = parser.parse_args()

num_sizes = 10
#          light pink pink       purple     dark blue  light blue cyan       green      yellow     orange     red
colours = ['#F56EF6', '#9400D3', '#4B0082', '#0000FF', '#4FA1FD', '#00FFFF', '#00FF00', '#E6C900', '#FF7F00', '#FF0000']
sizes = [320, 1056, 1472, 1792, 2048, 2304, 2528, 2720, 2912, 3072]
payloads_1 = [70252] * num_sizes
payloads_2 = [10976, 36223, 50493, 61470, 70252, 79033, 86717, 93303, 99889, 105378]
payloads_3 = [8253, 33016, 48264, 60373, 70252, 80278, 89158, 96843, 104589, 111089]
payloads_4 = [1715, 18677, 36292, 53786, 70252, 88912, 107042, 123919, 142030, 158067]

graph_title = ''
file_desc = ''
payloads = []
if args.rate == 1:
    payloads = payloads_1
    graph_title = 'Constant payload'
    file_desc = 'constant'
elif args.rate == 2:
    payloads = payloads_2
    graph_title = r'Payload $\propto \sqrt{N}$'
    file_desc = 'sqrt'
elif args.rate == 3:
    payloads = payloads_3
    graph_title = r'Payload $\propto \sqrt{N} \cdot \log{N}$'
    file_desc = 'sqrt_log'
else:
    payloads = payloads_4
    graph_title = r'Payload $\propto N$'
    file_desc = 'linear'

# Create plot
plt.figure(figsize=(7,7))

# Add curves to the plot
for i in range(0, num_sizes):
    roc_points_filename = \
        'roc/points/size{:d}_binary_{:d}b_roc.txt'.format(sizes[i], payloads[i])
    with open(roc_points_filename, 'r') as roc_points_file:
        lines = roc_points_file.readlines()
        x = []
        y = []
        min_pe_index = int(lines[-1]) - 1  # MATLAB is 1-indexed

        # Loop through all except the last line (which contains minPE index)
        for line in lines[:-1]:
            values = line.rstrip().split()
            x.append(float(values[0]))
            y.append(float(values[1]))

        plt.plot(x, y, color=colours[i], label=str(sizes[i]))
        plt.plot(x[min_pe_index], y[min_pe_index], color='k', marker='o', markersize=8)

plt.plot([0.0,1.0], [0.0,1.0], color='#696969', linestyle='dashed', label='Random')  # Random classifier
plt.xlabel(r'$P_{FA}$')
plt.ylabel(r'$1-P_{MD}$')
if args.with_title:
    plt.title(graph_title)
plt.legend()
plt.savefig('roc/curves/actor3_roc_{}.png'.format(file_desc))
