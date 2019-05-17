import argparse
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--rate', type=int, required=True,
                    help='Payload rate (0=all, 1=constant, 2=sqrt, ' \
                         '3=sqrt*log, 4=linear)')
parser.add_argument("-t", "--with-title", action='store_true',
                    help="Include graph title")
args = parser.parse_args()

# Number of pixels in each image size (x10^4)
x = [60.2112, 122.88, 176.9472, 240.8448, 304.8192, 355.1232, 420.5568, 491.52]

# 1 - MinPE for constant payload
# There is no datapoint for the 320x240 images with the large constant because
# (binary) embedding of more bits than pixels is impossible.
y1_s = [1-0.1038, 1-0.1866, 1-0.2327, 1-0.2722, 1-0.2984, 1-0.3130, 1-0.3323, 1-0.3395]
y1_m = [1-0.0516, 1-0.1221, 1-0.1699, 1-0.2028, 1-0.2375, 1-0.2498, 1-0.2691, 1-0.2866]
y1_l = [1-0.0261, 1-0.0800, 1-0.1215, 1-0.1556, 1-0.1878, 1-0.2096, 1-0.2187, 1-0.2392]

# 1 - MinPE for payload proportional to sqrt(N)
y2_s = [1-0.2273, 1-0.2403, 1-0.2597, 1-0.2722, 1-0.2717, 1-0.2780, 1-0.2840, 1-0.2866]
y2_m = [1-0.1665, 1-0.1832, 1-0.1927, 1-0.2028, 1-0.2137, 1-0.2206, 1-0.2181, 1-0.2230]
y2_l = [1-0.1159, 1-0.1354, 1-0.1546, 1-0.1556, 1-0.1667, 1-0.1717, 1-0.1732, 1-0.1730]

# 1 - MinPE for payload proportional to sqrt(N) * log(N)
y3_s = [1-0.2474, 1-0.2503, 1-0.2743, 1-0.2722, 1-0.2731, 1-0.2737, 1-0.2773, 1-0.2787]
y3_m = [1-0.1801, 1-0.1914, 1-0.1912, 1-0.2028, 1-0.2108, 1-0.2125, 1-0.2117, 1-0.2151]
y3_l = [1-0.1350, 1-0.1387, 1-0.1522, 1-0.1556, 1-0.1638, 1-0.1627, 1-0.1669, 1-0.1697]

# 1 - MinPE for payload proportional to N
y4_s = [1-0.3401, 1-0.3030, 1-0.2945, 1-0.2722, 1-0.2483, 1-0.2439, 1-0.2309, 1-0.2230]
y4_m = [1-0.2842, 1-0.2379, 1-0.2241, 1-0.2028, 1-0.1938, 1-0.1839, 1-0.1709, 1-0.1613]
y4_l = [1-0.2409, 1-0.1955, 1-0.1776, 1-0.1556, 1-0.1463, 1-0.1346, 1-0.1233, 1-0.1100]

x_label = r'Cover size N (pixels) $\times 10^4$'
y_label = r'$1-P_E$'
axis_bounds = [0,800,0.5,1.0]

if args.rate == 0:  # Plot all four payload rates
    # Create plot
    plt.figure(figsize=(12,10))

    # Constant payload
    plt.subplot(2,2,1)
    plt.plot(x, y1_s, 'r+:', label=r'$0.7 r_1$')
    plt.plot(x, y1_m, 'bs:', label=r'$r_1$')
    plt.plot(x, y1_l, 'go:', label=r'$1.3 r_1$')
    plt.axis(axis_bounds)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if args.with_title:
        plt.title(r'Constant payload')
    plt.legend(loc='upper right')

    # Payload proportional to sqrt(N)
    plt.subplot(2,2,2)
    plt.plot(x, y2_s, 'r+:', label=r'$0.7 r_2$')
    plt.plot(x, y2_m, 'bs:', label=r'$r_2$')
    plt.plot(x, y2_l, 'go:', label=r'$1.3 r_2$')
    plt.axis(axis_bounds)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if args.with_title:
        plt.title(r'Payload $\propto \sqrt{N}$')
    plt.legend(loc='upper right')

    # Payload proportional to sqrt(N) * log(N)
    plt.subplot(2,2,3)
    plt.plot(x, y3_s, 'r+:', label=r'$0.7 r_3$')
    plt.plot(x, y3_m, 'bs:', label=r'$r_3$')
    plt.plot(x, y3_l, 'go:', label=r'$1.3 r_3$')
    plt.axis(axis_bounds)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if args.with_title:
        plt.title(r'Payload $\propto \sqrt{N} \cdot \log{N}$')
    plt.legend(loc='upper right')

    # Payload proportional to N
    plt.subplot(2,2,4)
    plt.plot(x, y4_s, 'r+:', label=r'$0.7 r_4$')
    plt.plot(x, y4_m, 'bs:', label=r'$r_4$')
    plt.plot(x, y4_l, 'go:', label=r'$1.3 r_4$')
    plt.axis(axis_bounds)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if args.with_title:
        plt.title(r'Payload $\propto N$')
    plt.legend(loc='upper right')

    # Save plot
    plt.tight_layout()
    plt.savefig('bossbase_detectability_all_payload_rates.png')

else:
    graph_title = ''
    file_desc = ''
    y_small = []
    y_med = []
    y_large = []
    constant_name = ''

    if args.rate == 1:  # Constant payload
        y_small = y1_s
        y_med = y1_m
        y_large = y1_l
        graph_title = r'Constant payload'
        file_desc = 'constant'
        constant_name = r'$r_1$'
    elif args.rate == 2:  # Payload proportional to sqrt(N)
        y_small = y2_s
        y_med = y2_m
        y_large = y2_l
        graph_title = r'Payload $\propto \sqrt{N}$'
        file_desc = 'sqrt'
        constant_name = r'$r_2$'
    elif args.rate == 3:  # Payload proportional to sqrt(N) * log(N)
        y_small = y3_s
        y_med = y3_m
        y_large = y3_l
        graph_title = r'Payload $\propto \sqrt{N} \cdot \log{N}$'
        file_desc = 'sqrt_log'
        constant_name = r'$r_3$'
    else:  # Payload proportional to N
        y_small = y4_s
        y_med = y4_m
        y_large = y4_l
        graph_title = r'Payload $\propto N$'
        file_desc = 'linear'
        constant_name = r'$r_4$'

    # Create plot
    plt.figure(figsize=(6,5))
    plt.plot(x, y_small, 'r+:', label=r'$0.7${}'.format(constant_name))
    plt.plot(x, y_med, 'bs:', label=constant_name)
    plt.plot(x, y_large, 'go:', label=r'$1.3${}'.format(constant_name))
    plt.axis(axis_bounds)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if args.with_title:
        plt.title(graph_title)
    plt.legend(loc='upper right')

    # Save plot
    plt.tight_layout()
    plt.savefig('bossbase_detectability_{}.png'.format(file_desc))
