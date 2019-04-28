import matplotlib.pyplot as plt

# Number of pixels in each image size (x10^4)
x = [7.68, 83.6652, 162.5088, 240.8448, 314.5728, 398.1312, 479.3088, 554.88, 635.9808, 707.7888]

# O(1)
y1 = [1-0.0,1-0.0457,1-0.1064,1-0.1638,1-0.2023,1-0.2352,1-0.2625,1-0.2767,1-0.2907,1-0.3099]

# O(sqrt(n))
y2 = [1-0.0674,1-0.1574,1-0.1842,1-0.1918,1-0.2023,1-0.2054,1-0.2115,1-0.2053,1-0.2054,1-0.2081]

# O(sqrt(n) * log(n))
y3 = [1-0.1268,1-0.1809,1-0.1953,1-0.1963,1-0.2023,1-0.2017,1-0.2030,1-0.1962,1-0.1965,1-0.1950]

# O(n)
y4 = [1-0.4205,1-0.3237,1-0.2655,1-0.2252,1-0.2023,1-0.1729,1.0-0.1551,1-0.1367,1-0.1233,1-0.1170]

# Create and save plot
plt.figure(figsize=(12,10))
plt.plot(x, y1, 'r+:', label='O(1)')
plt.plot(x, y2, 'bs:', label='O(sqrt n)')
plt.plot(x, y3, 'go:', label='O(sqrt n * log n)')
plt.plot(x, y4, 'c*:', label='O(n)')
plt.axis([0,800,0.5,1.0])
plt.xlabel(r'Cover size N in pixels ($\times 10^4$)')
plt.ylabel(r'$1-P_E$')
plt.title(r'Combined results')
plt.legend()
plt.savefig('combined_graph_27_02_2019.png')
