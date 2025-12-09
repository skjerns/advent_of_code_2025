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

content = get_input(filename=__file__)
content = get_example(filename=__file__)


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
