#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 06:58:39 2025

@author: simon
"""
import scipy
import numpy as np
from tqdm import tqdm
from aoc import get_input, get_lines, get_matrix, lines2matrix, input2matrix

matrix = get_matrix(4)

matrix2 = input2matrix("""..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.""")


# convert to something sensible

matrix[matrix=='.'] = 0
matrix[matrix=='@'] = 1
matrix = matrix.astype(int)

#%% part 1
kernel = np.ones([3, 3])
convolved = scipy.signal.convolve2d(matrix, kernel, 'same')

# count what is below 5 but over 0, but only for paper coil positions
accessible = (convolved[matrix.astype(bool)]<5).sum()

print(f'{accessible=}')

#%% part 2

kernel = np.ones([3, 3])

removed = 0

# keep removing until there's nothing left to remove
while True:
    x = scipy.signal.convolve2d(matrix, kernel, 'same')

    # limit convolved to positions of coils
    x[matrix==0] = np.inf

    # see where we can remove toilet roles in this round
    idx = np.where(x<5)

    if len(idx[0]):
        # remove all of the roles and then check again
        matrix[idx] = 0
        removed += len(idx[0])
    else:
        # nothing more to remove!
        break

print(f'{removed=}')
