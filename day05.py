#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 08:30:48 2025

@author: simon
"""

import numpy as np
from tqdm import tqdm
from aoc import get_input, get_lines, get_matrix, lines2matrix


content = get_input(5)


content2 = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

# transform into something useful

ranges, ids = content.split('\n\n')

ranges = [[int(x) for x in r.split('-')] for r in ranges.split('\n')]
ranges = [range(r[0], r[1]+1) for r in ranges]

ids = [int(x) for x in ids.split('\n')]

#%% part 1

fresh = 0
for x in ids:
    if any([x in r for r in ranges]):
        fresh +=1
        continue

print(f'{fresh=}')


#%% part 2

# merge all ranges

ranges = sorted(ranges, key=lambda x: x.start)

while True:
    # walk through each range and see if we can merge
    stop=False
    ranges = sorted(ranges, key=lambda x: x.start)
    for i, r1 in enumerate(ranges):
        if stop:
            break
        for j, r2 in enumerate(ranges[1+i:], i+1):
            if r1.stop>=r2.start:
                # merge these two ranges and start from anew
                ranges.pop(j)
                ranges[i] = range(r1.start, max(r2.stop, r1.stop))
                stop = True
                break

    if i==len(ranges)-1:
        break

fresh = sum([len(r) for r in ranges])
print(f'{fresh=}')
# 311541667160941 too low
