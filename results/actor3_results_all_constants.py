import matplotlib.pyplot as plt

# Number of pixels in each image size (x10^4)
x = [7.68, 83.6652, 162.5088, 240.8448, 314.5728, 398.1312, 479.3088, 554.88, 635.9808, 707.7888]

# O(1)
# There is no datapoint for the large constant because (binary) embedding of
# more bits than pixels is impossible.
y1_s = [1-0.0,1-0.0991,1-0.1909,1-0.2497,1-0.2928,1-0.3227,1-0.3404,1-0.3538,1-0.3674,1-0.3828]
y1_m = [1-0.0,1-0.0457,1-0.1064,1-0.1638,1-0.2023,1-0.2352,1-0.2625,1-0.2767,1-0.2907,1-0.3099]
y1_l = [1.0,1-0.0217,1-0.0596,1-0.1033,1-0.1344,1-0.1664,1-0.1962,1-0.2101,1-0.2254,1-0.2444]

# O(sqrt(n))
y2_s = [1-0.1428,1-0.2476,1-0.2700,1-0.2833,1-0.2928,1-0.2949,1-0.2956,1-0.2920,1-0.2921,1-0.2985]
y2_m = [1-0.0674,1-0.1574,1-0.1842,1-0.1918,1-0.2023,1-0.2054,1-0.2115,1-0.2053,1-0.2054,1-0.2081]
y2_l = [1-0.0320,1-0.1053,1-0.1205,1-0.1343,1-0.1344,1-0.1394,1-0.1395,1-0.1427,1-0.1448,1-0.1475]

# O(sqrt(n) * log(n))
y3_s = [1-0.2037,1-0.2721,1-0.2788,1-0.2865,1-0.2928,1-0.2916,1-0.2909,1-0.2820,1-0.2804,1-0.2849]
y3_m = [1-0.1268,1-0.1809,1-0.1953,1-0.1963,1-0.2023,1-0.2017,1-0.2030,1-0.1962,1-0.1965,1-0.1950]
y3_l = [1-0.0714,1-0.1277,1-0.1301,1-0.1383,1-0.1344,1-0.1364,1-0.1307,1-0.1340,1-0.1324,1-0.1347]

# O(n)
y4_s = [1-0.4467,1-0.3809,1-0.3385,1-0.3137,1-0.2928,1-0.2667,1-0.2439,1-0.2234,1-0.2099,1-0.1960]
y4_m = [1-0.4205,1-0.3237,1-0.2655,1-0.2252,1-0.2023,1-0.1729,1-0.1551,1-0.1367,1-0.1233,1-0.1170]
y4_l = [1-0.3887,1-0.2566,1-0.2003,1-0.1650,1-0.1344,1-0.1118,1-0.0930,1-0.0841,1-0.0727,1-0.0714]

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
plt.savefig('actor3_full_graph_29_03_2019.png')
