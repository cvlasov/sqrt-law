"""
Given the costs of changing each coefficient (c_1...c_N) and the length
of the payload to embed (m), this script computes the probabilities
(pi_1...pi_N) with which each coefficient should be changed in order
to simulate the embedding of an m-bit payload.
"""

import argparse
import math
import numpy as np
import time

# HELPER FUNCTIONS

def H2_scalar(x):
    """
    Computes the entropy of a scalar.
    """
    if   x == 0: return - (1-x) * math.log(1-x,2)
    elif x == 1: return - x * math.log(x,2)
    else:        return - x * math.log(x,2) - (1-x) * math.log(1-x,2)

"""Vectorized version of H2_scalar"""
H2 = np.vectorize(H2_scalar)

def entropy_sum(probabilities):
    """
    Computes the sum of the entropies of the given probabilities.
    """
    return np.sum(H2(probabilities))

def compute_probabilities(costs, lam):
    """
    Computes the probability of modifying each coefficient, given the cost of
    modifying each one and the value of lambda.
    """
    return 1 / (1 + np.exp(lam*costs))

##########
# SCRIPT #
##########
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bits", type=int, required=True,
                    help="Number of bits in the payload")
parser.add_argument("-c", "--costs", type=argparse.FileType('r'),
                    default='costs.txt', help="File with costs")
parser.add_argument("-o", "--outputfile", type=argparse.FileType('w'),
                    default='probabilities.txt',
                    help="File where probabilities will be written")
parser.add_argument("-v", "--verbose", action='store_true',
                    help="Print intermediate computation results")
args = parser.parse_args()

start = time.time()

# Get costs
cost_list = []

for line in args.costs:
    for c in line.split():
        cost_list.append(float(c))

costs = np.array(cost_list)

# Exponential search to find an upper (and lower) bound on lambda
m = args.bits
lam = 0
low = -1
high = -1
if args.verbose: print('------------------')
if args.verbose: print('EXPONENTIAL SEARCH')

while (True):
    probs = compute_probabilities(costs, lam)
    H_sum = entropy_sum(probs)
    if args.verbose: print('sum with lambda=' + str(lam) + ' is ' + str(H_sum))
    if H_sum < m:
        low = 0 if lam == 1 else int(lam/10)
        high = lam
        break
    lam = 1 if lam == 0 else lam*10

if args.verbose: print('=> lambda is in [' + str(low) + ', ' + str(high) + ')')

# Binary search to find lambda s.t. sum of all H(pi_i) is >= m and < m+1
if args.verbose: print('-------------')
if args.verbose: print('BINARY SEARCH')
probs = np.array([])

while (low <= high):
    lam = (high+low) / 2
    probs = compute_probabilities(costs, lam)
    H_sum = entropy_sum(probs)
    if args.verbose: print('sum with lambda=' + str(lam) + ' is ' + str(H_sum))
    if m <= H_sum and H_sum < m+1:
        break
    elif H_sum < m:
        high = lam
    else:
        low = lam

if args.verbose: print('=> chosen lambda: ' + str(lam))

# Write probabilities to text file, one value per line
for p in probs:
    args.outputfile.write(str(p) + '\n')

end = time.time()
print(str(end-start) + ' seconds elapsed')
