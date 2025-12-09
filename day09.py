#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 07:36:38 2025

@author: simon
"""

import numpy as np
from tqdm import tqdm
from aoc import get_input, get_lines, get_matrix, lines2matrix, input2matrix
from aoc import get_example, mem
import matplotlib.pyplot as plt
from scipy.ndimage import binary_fill_holes
import scipy

content = get_input(filename=__file__)
content2 = get_example(filename=__file__)


lines = content.split('\n')

coords = [np.array([int(n) for n in x.split(',')]) for x in lines]

#%% part 1

maxarea = 0

for i, c1 in enumerate(coords):
    for c2 in coords[i+1:]:  # only calculate for the diagonal
        area = np.prod(abs(c1-c2+1))
        if area>maxarea:
            maxarea = area

print(f'{maxarea=}')

#%% part 2

# idea: first create the matrix
# NOPE, scratch that, not enough RAM

matrix = np.zeros(np.max(coords, 0)+1, dtype=bool)

for c1, c2 in zip(coords[:-1], coords[1:]):
    x1, x2 = sorted([c1[0], c2[0]])
    y1, y2 = sorted([c1[1], c2[1]])
    if x1==x2:
        matrix[x1, y1: y2+1] = True
    elif y1==y2:
        matrix[x1: x2+1, y1] = True
    else:
        raise Exception

# add last one as well that is not covered by zip
c1, c2 = coords[0], coords[-1]
x1, x2 = sorted([c1[0], c2[0]])
y1, y2 = sorted([c1[1], c2[1]])
if x1==x2:
    matrix[x1, y1: y2+1] = True
elif y1==y2:
    matrix[x1: x2+1, y1] = True


asd
# next color inside as well
# OH NO THAT CRASHES MY RAM
# matrix = binary_fill_holes(matrix)

# plt.matshow(matrix)

# next do our calculation once again, but this time in stupid and slow
maxarea = 0
for i, c1 in enumerate(tqdm(coords)):
    for c2 in coords[i+1:]:  # only calculate for the diagonal

        x1, x2 = sorted([c1[0], c2[0]])
        y1, y2 = sorted([c1[1], c2[1]])
        asd
        if matrix[x1:x2+1, y1:y2+1].all():
            if area>maxarea:
                maxarea = area
