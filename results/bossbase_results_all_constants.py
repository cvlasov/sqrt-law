import matplotlib.pyplot as plt

# Number of pixels in each image size (x10^4)
x = [60.2112, 122.88, 176.9472, 240.8448, 304.8192, 354.4704, 420.5568, 491.52]

# O(1)
y1_s = [1-0.1038, 1-0.1866, 1-0.2327, 1-0.2722, 1-0.2984, 0.5, 1-0.3323, 1-0.3395]
y1_m = [1-0.0516, 1-0.1221, 1-0.1699, 1-0.2028, 1-0.2375, 0.5, 1-0.2691, 1-0.2866]
y1_l = [1-0.0261, 1-0.0800, 1-0.1215, 1-0.1556, 1-0.1878, 0.5, 1-0.2187, 1-0.2392]

# O(sqrt(n))
y2_s = [1-0.2273, 1-0.2403, 1-0.2597, 1-0.2722, 1-0.2717, 0.5, 1-0.2840, 1-0.2866]
y2_m = [1-0.1665, 1-0.1832, 1-0.1927, 1-0.2028, 1-0.2137, 0.5, 1-0.2181, 1-0.2230]
y2_l = [1-0.1159, 1-0.1354, 1-0.1546, 1-0.1556, 1-0.1667, 0.5, 1-0.1732, 0.5]

# O(sqrt(n) * log(n))
y3_s = [1-0.2474, 1-0.2503, 1-0.2743, 1-0.2722, 1-0.2731, 0.5, 1-0.2773, 1-0.2787]
y3_m = [1-0.1801, 1-0.1914, 1-0.5000, 1-0.2028, 1-0.2108, 0.5, 1-0.2117, 1-0.2151]
y3_l = [1-0.1350, 1-0.5000, 1-0.5000, 1-0.1556, 1-0.1638, 0.5, 1-0.1669, 0.5]

# O(n)
y4_s = [1-0.3401, 1-0.3030, 1-0.2945, 1-0.2722, 1-0.2483, 0.5, 1-0.2309, 1-0.2230]
y4_m = [1-0.2842, 1-0.2379, 1-0.2241, 1-0.2028, 1-0.1938, 0.5, 1-0.1709, 1-0.1613]
y4_l = [1-0.2409, 1-0.1955, 1-0.1776, 1-0.1556, 1-0.1463, 0.5, 1-0.1233, 0.5]

# Create plot
plt.figure(figsize=(12,10))
x_label = r'Cover size N (pixels) $\times 10^4$'
y_label = r'$1-P_E$'
axis_bounds = [0,800,0.5,1.0]

# O(1) graph
plt.subplot(2,2,1)
plt.plot(x, y1_s, 'r+:', label='small constant')
plt.plot(x, y1_m, 'bs:', label='original constant')
plt.plot(x, y1_l, 'go:', label='big constant')
plt.axis(axis_bounds)
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.title(r'Constant payload')
plt.legend()

# O(sqrt(n)) graph
plt.subplot(2,2,2)
plt.plot(x, y2_s, 'r+:', label='small constant')
plt.plot(x, y2_m, 'bs:', label='original constant')
plt.plot(x, y2_l, 'go:', label='big constant')
plt.axis(axis_bounds)
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.title(r'Payload $\propto \sqrt{N}$')
plt.legend()

# O(sqrt(n) * log(n)) graph
plt.subplot(2,2,3)
plt.plot(x, y3_s, 'r+:', label='small constant')
plt.plot(x, y3_m, 'bs:', label='original constant')
plt.plot(x, y3_l, 'go:', label='big constant')
plt.axis(axis_bounds)
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.title(r'Payload $\propto \sqrt{N} \cdot \log{N}$')
plt.legend()

# O(n) graph
plt.subplot(2,2,4)
plt.plot(x, y4_s, 'r+:', label='small constant')
plt.plot(x, y4_m, 'bs:', label='original constant')
plt.plot(x, y4_l, 'go:', label='big constant')
plt.axis(axis_bounds)
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.title(r'Payload $\propto N$')
plt.legend()

# Save plot
plt.tight_layout()
plt.savefig('bossbase_full_graph_14_05_2019_NEW.png')
