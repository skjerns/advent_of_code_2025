#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 09:29:00 2025

@author: simon
"""

import numpy as np
from tqdm import tqdm
from aoc import get_input, get_lines, get_matrix, lines2matrix, input2matrix
from aoc import get_example, mem
from tqdm import tqdm
from functools import cache
from scipy.spatial.distance import pdist, squareform, euclidean
from itertools import combinations

content = get_input(filename=__file__)

content2 = get_example(filename=__file__)


lines = content.split('\n')

matrix = np.array([line.split(',') for line in lines], dtype=int)

coords = [tuple([int(x) for x in coord]) for coord in matrix]


#%% part 1
dists = squareform(pdist(coords))

dists[dists==0] = np.inf

circuits = [{x} for x in coords]

for i in tqdm(range(1000)):
    # print('')
    if np.isinf(dists).all():
        break
    # get smallest distance
    x, y = np.unravel_index(np.argmin(dists), dists.shape)

    # remove this distances
    dists[x, y] = np.inf
    dists[y, x] = np.inf

    # get nodes that we want to connect
    n1 = coords[x]
    n2 = coords[y]


    c1 = None
    c2 = None
    # find the circuit in which these two are
    for i, circ in enumerate(circuits):
        if n1 in circ:
            c1 = circ
        if n2 in circ:
            c2 = circ

    if c1==c2:  # nothing to do
        # print('Nothing to do for {n1} and {n2}!')
        # print(f'{circuits=}')
        # print('\n', len(circuits))
        continue

    # merge the two
    c3 = c1.union(c2)

    circuits.remove(c1)
    circuits.remove(c2)
    circuits += [c3]
    # print(f'connect {n1} and {n2}')
    # print(f'{circuits=}')
    # print(len(circuits))
    continue


lens = sorted([len(x) for x in circuits])
print(f'{lens=}')

print(f'product of largest three = {np.prod(lens[-3:])}')

#%% part 2

dists = squareform(pdist(coords))

dists[dists==0] = np.inf

circuits = [{x} for x in coords]

while True:
    # print('')
    if np.isinf(dists).all():
        break
    # get smallest distance
    x, y = np.unravel_index(np.argmin(dists), dists.shape)

    # remove this distances
    dists[x, y] = np.inf
    dists[y, x] = np.inf

    # get nodes that we want to connect
    n1 = coords[x]
    n2 = coords[y]


    c1 = None
    c2 = None
    # find the circuit in which these two are
    for i, circ in enumerate(circuits):
        if n1 in circ:
            c1 = circ
        if n2 in circ:
            c2 = circ

    if c1==c2:  # nothing to do
        # print('Nothing to do for {n1} and {n2}!')
        # print(f'{circuits=}')
        # print('\n', len(circuits))
        continue

    # merge the two
    c3 = c1.union(c2)

    circuits.remove(c1)
    circuits.remove(c2)
    circuits += [c3]
    # print(f'connect {n1} and {n2}')
    # print(f'{circuits=}')
    # print(len(circuits))
    if len(circuits)==1:
        break


print(f'last two boxes are {n1}, {n2}')
print(f'{n1[0]*n2[0]}')
