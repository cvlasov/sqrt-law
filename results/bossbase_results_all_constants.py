import matplotlib.pyplot as plt

# Number of pixels in each image size (x10^4)
x = [60.2112, 122.88, 176.9472, 240.8448, 304.8192, 354.4704, 420.5568, 491.52]

# O(1)
y1_s = [1-0.1038, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
y1_m = [1-0.0516, 0.5, 0.5, 1-0.2028, 0.5, 0.5, 0.5, 0.5]
y1_l = [1-0.0261, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

# O(sqrt(n))
y2_s = [1-0.2273, 1-0.2403, 1-0.2597, 1-0.5000, 1-0.2717, 0.5, 0.5, 0.5]
y2_m = [1-0.1665, 1-0.1832, 1-0.1927, 1-0.2028, 1-0.2137, 0.5, 0.5, 0.5]
y2_l = [1-0.1159, 1-0.1354, 1-0.1546, 0.5, 0.5, 0.5, 0.5, 0.5]

# O(sqrt(n) * log(n))
y3_s = [1-0.2474, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
y3_m = [1-0.1801, 0.5, 0.5, 1-0.2028, 0.5, 0.5, 0.5, 0.5]
y3_l = [1-0.1350, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

# O(n)
y4_s = [1-0.3401, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
y4_m = [1-0.2842, 0.5, 0.5, 1-0.2028, 0.5, 0.5, 0.5, 0.5]
y4_l = [1-0.2409, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

# Create plot
plt.figure(figsize=(12,10))

# O(1) graph
plt.subplot(2,2,1)
plt.plot(x, y1_s, 'r+:', label='small constant')
plt.plot(x, y1_m, 'bs:', label='original constant')
plt.plot(x, y1_l, 'go:', label='big constant')
plt.axis([0,800,0.5,1.0])
plt.xlabel(r'Cover size N in pixels ($\times 10^4$)')
plt.ylabel(r'$1-P_E$')
plt.title(r'$O(1)$')
plt.legend()

# O(sqrt(n)) graph
plt.subplot(2,2,2)
plt.plot(x, y2_s, 'r+:', label='small constant')
plt.plot(x, y2_m, 'bs:', label='original constant')
plt.plot(x, y2_l, 'go:', label='big constant')
plt.axis([0,800,0.5,1.0])
plt.xlabel(r'Cover size N in pixels ($\times 10^4$)')
plt.ylabel(r'$1-P_E$')
plt.title(r'$O(\sqrt{N})$')
plt.legend()

# O(sqrt(n) * log(n)) graph
plt.subplot(2,2,3)
plt.plot(x, y3_s, 'r+:', label='small constant')
plt.plot(x, y3_m, 'bs:', label='original constant')
plt.plot(x, y3_l, 'go:', label='big constant')
plt.axis([0,800,0.5,1.0])
plt.xlabel(r'Cover size N in pixels ($\times 10^4$)')
plt.ylabel(r'$1-P_E$')
plt.title(r'$O(\sqrt{N}\log{N})$')
plt.legend()

# O(n) graph
plt.subplot(2,2,4)
plt.plot(x, y4_s, 'r+:', label='small constant')
plt.plot(x, y4_m, 'bs:', label='original constant')
plt.plot(x, y4_l, 'go:', label='big constant')
plt.axis([0,800,0.5,1.0])
plt.xlabel(r'Cover size N in pixels ($\times 10^4$)')
plt.ylabel(r'$1-P_E$')
plt.title(r'$O(N)$')
plt.legend()

# Save plot
plt.tight_layout()
plt.savefig('bossbase_full_graph_03_05_2019.png')
