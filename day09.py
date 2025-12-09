#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 07:36:38 2025

@author: simon
"""
import gc
import stimer
from stimer import ContextProfiler
import numpy as np
from tqdm import tqdm
from aoc import get_input, get_lines, get_matrix, lines2matrix, input2matrix
from aoc import get_example, mem
import matplotlib.pyplot as plt
from scipy.ndimage import binary_closing, label, binary_propagation
import scipy
from joblib import Parallel, delayed

content = get_input(filename=__file__)
content2 = get_example(filename=__file__)


lines = content.split('\n')

coords = [np.array([int(n) for n in x.split(',')]) for x in lines]

#%% part 1
with stimer('day 09 part 1'):

    maxarea = 0

    for i, c1 in enumerate(coords):
        for c2 in coords[i+1:]:  # only calculate for the diagonal
            area = np.prod(abs(c1-c2+1))
            if area>maxarea:
                maxarea = area

    print(f'{maxarea=}')



#%% part 2
# with ContextProfiler():
# idea: first create the matrix
# NOPE, scratch that, not enough RAM

# matrix = np.zeros(np.max(coords, 0)+2, dtype=bool)

# for c1, c2 in zip(coords[:-1], coords[1:]):
#     x1, x2 = sorted([c1[0], c2[0]])
#     y1, y2 = sorted([c1[1], c2[1]])
#     if x1==x2:
#         matrix[x1, y1: y2+1] = True
#     elif y1==y2:
#         matrix[x1: x2+1, y1] = True
#     else:
#         raise Exception

# # add last one as well that is not covered by zip
# c1, c2 = coords[0], coords[-1]
# x1, x2 = sorted([c1[0], c2[0]])
# y1, y2 = sorted([c1[1], c2[1]])
# if x1==x2:
#     matrix[x1, y1: y2+1] = True
# elif y1==y2:
#     matrix[x1: x2+1, y1] = True

# # label to get the inside of the component
# inv = (matrix == 0)
# labels, n = label(inv)
# matrix[labels==2] = True

# # next do our calculation once again, but this time in stupid and slow
# maxarea = 0


# for i, c1 in enumerate(tqdm(coords)):
#     for j, c2 in enumerate(coords[i+1:]):  # only calculate for the diagonal

#         area = np.prod(abs(c1-c2+1))

#         if area<maxarea:
#             continue # don't need to check it.

#         x1, x2 = sorted([c1[0], c2[0]])
#         y1, y2 = sorted([c1[1], c2[1]])
#         if matrix[x1:x2+1, y1:y2+1].all():
#             maxarea = area
# print(f'{maxarea=}')


#%% part 2 parallel
stimer.start()
matrix = np.zeros(np.max(coords, 0)+2, dtype=bool)

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

# label to get the inside of the component
inv = (matrix == 0)
labels, n = label(inv)
matrix[labels==2] = True
del labels

# next do our calculation once again, but this time in stupid and slow

gc.collect()

to_check = []

for i, c1 in enumerate(tqdm(coords, 'precalculating rectangles')):
    for j, c2 in enumerate(coords[i+1:]):  # only calculate for the diagonal

        x1, x2 = sorted([c1[0], c2[0]])
        y1, y2 = sorted([c1[1], c2[1]])

        to_check.append((x1, x2, y1, y2))


def calcmax(coords):
    maxarea = 0
    for x1, x2, y1, y2 in coords:
        area = (x2-x1+1) * (y2-y1+1)
        if area<maxarea:
            continue
        if matrix[x1:x2+1, y1:y2+1].all():
            maxarea = area
    return maxarea

# warning, this takes more than 40GB of RAM and is very stupid
from more_itertools import chunked
n_jobs = 12
chunks = list(chunked(to_check, n_jobs*100))
res = Parallel(n_jobs)(delayed(calcmax)(x) for x in tqdm(chunks))
print(f'{res}')
print(f'{max(res)}=')
stimer.stop()
