"""
SCRIPT RESULTS
Actor3 O(sqrt(N)) slope          = -0.00013655
Actor3 O(sqrt(N)*log(N)) slope   = -0.00005756
BOSSbase O(sqrt(N)) slope        = -0.00012949
BOSSbase O(sqrt(N)*log(N)) slope = -0.00008175
"""

def compute_slope(xs, ys):
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    slope = sum(map(lambda x,y : (x - x_mean) * (y - y_mean), xs, ys)) \
            / sum(map(lambda x : (x - x_mean)**2, xs))
    return slope

def print_slope(name, rate, slope):
    print('{} O({}) slope = {:.8f}'.format(name, rate, float(slope)))

# Actor3 number of pixels (x10^4)
a3_x = [7.68, 83.6652, 162.5088, 240.8448, 314.5728, 398.1312, 479.3088, 554.88, 635.9808, 707.7888]

# Actor3 number of pixels (x10^4)
bb_x = [60.2112, 122.88, 176.9472, 240.8448, 304.8192, 355.1232, 420.5568, 491.52]

# Actor3 O(sqrt(N)) detectability
a3_sqrt = [1-0.0674,1-0.1574,1-0.1842,1-0.1918,1-0.2023,1-0.2054,1-0.2115,1-0.2053,1-0.2054,1-0.2081]
a3_sqrt_slope = compute_slope(a3_x, a3_sqrt)
print_slope('Actor3','sqrt(N)', a3_sqrt_slope)

# Actor3 O(sqrt(N)*log(N)) detectability
a3_sqrt_log = [1-0.1268,1-0.1809,1-0.1953,1-0.1963,1-0.2023,1-0.2017,1-0.2030,1-0.1962,1-0.1965,1-0.1950]
a3_sqrt_log_slope = compute_slope(a3_x, a3_sqrt_log)
print_slope('Actor3','sqrt(N)*log(N)', a3_sqrt_log_slope)

# BOSSbase O(sqrt(N)) detectability
bb_sqrt = [1-0.1665, 1-0.1832, 1-0.1927, 1-0.2028, 1-0.2137, 1-0.2206, 1-0.2181, 1-0.2230]
bb_sqrt_slope = compute_slope(bb_x, bb_sqrt)
print_slope('BOSSbase','sqrt(N)', bb_sqrt_slope)

# BOSSbase O(sqrt(N)*log(N)) detectability
bb_sqrt_log = [1-0.1801, 1-0.1914, 1-0.1912, 1-0.2028, 1-0.2108, 1-0.2125, 1-0.2117, 1-0.2151]
bb_sqrt_log_slope = compute_slope(bb_x, bb_sqrt_log)
print_slope('BOSSbase','sqrt(N)*log(N)', bb_sqrt_log_slope)
