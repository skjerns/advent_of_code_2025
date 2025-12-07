#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 08:16:24 2025

@author: simon
"""

import numpy as np
from tqdm import tqdm
from aoc import get_input, get_lines, get_matrix, lines2matrix, input2matrix
from aoc import get_example, mem
from tqdm import tqdm

content = get_input(filename=__file__)

content2 = get_example(filename=__file__)

matrix = input2matrix(content)

#%% part 1

start = np.squeeze(np.where(matrix=='S'))

splitters = set()

matrix_p1 = matrix.copy()

def step(pos):
    if any(pos<0) or any(pos>=matrix_p1.shape):
        return
    curr = matrix_p1[*pos]
    if curr=='.' or curr=='S':
        matrix_p1[*pos] = '|'
        step(pos + [1, 0])
    elif curr=='^':
        splitters.add(str(pos))
        step(pos + [0, -1])
        step(pos + [0, 1])
    elif curr=='|':
        return
    else:
        raise Exception(f'unknown {curr=}')

step(start)

print(f'{len(splitters)=}')

#%% part 2
from functools import cache

y, x = list(np.squeeze(np.where(matrix=='S')))

# convert to boolean for faster calculation
matrix[matrix=='S'] = 0
matrix[matrix=='.'] = 0
matrix[matrix=='^'] = 1
matrix = matrix.astype(int).astype(bool)


@cache
def step(x, y):
    # for this function, we want to know for an arbitrary position,
    # how many junctions are below it. then cache this function

    if x<0 or y<0 or y>=matrix.shape[0] or x>=matrix.shape[1]:
        return 0 # one path, recursion break!

    curr = matrix[y, x]
    if curr:  # True means splitter, so split!
        count = step(x-1, y)
        count += step(x+1, y) + 1
    else:
        # else simply descend downward
        count = step(x, y+1)
    return count

splitter_count = step(x, y) + 1

print(f'{splitter_count=}')
