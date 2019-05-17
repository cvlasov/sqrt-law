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
# light pink, pink, purple, dark blue, light blue, cyan, green, yellow, orange,
# red
colours = ['#F56EF6', '#9400D3', '#4B0082', '#0000FF', '#4FA1FD', '#00FFFF',
           '#00FF00', '#E6C900', '#FF7F00', '#FF0000']
sizes = [320, 1056, 1472, 1792, 2048, 2304, 2528, 2720, 2912, 3072]
payloads_1 = [91327] * num_sizes
payloads_2 = [14269, 47090, 65641, 79911, 91327, 102743, 112732, 121294, 129856,
              136991]
payloads_3 = [10728, 42921, 62744, 78485, 91327, 104361, 115905, 125895, 135966,
              144416]
payloads_4 = [2229, 24281, 47180, 69922, 91327, 115586, 139154, 161094, 184640,
              205487]

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
        plt.plot(x[min_pe_index], y[min_pe_index], color='k', marker='o',
                 markersize=8)

# Plot ROC curve of a random classifier for reference
plt.plot([0.0,1.0], [0.0,1.0], color='#696969', linestyle='dashed')

plt.xlabel(r'$f_p$')
plt.ylabel(r'$1-f_n$')
if args.with_title:
    plt.title(graph_title)

# Place legend in bottom-right corner of plot
plt.legend(loc='lower right', bbox_to_anchor=(1.0, 0.0))

# Save plot
plt.savefig('roc/curves/actor3_roc_{}_large_constant.png'.format(file_desc))
