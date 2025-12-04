#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 07:16:12 2025

@author: simon
"""
import numpy as np
from tqdm import tqdm
from aoc import get_input, get_lines, get_matrix, lines2matrix

matrix = get_matrix(3).astype(int)

matrix2 = lines2matrix(("""987654321111111
811111111111119
234234234234278
818181911112111""").split('\n')).astype(int)


#%% part 1

joltages = []
for battery in matrix:
    idx = np.argsort(battery)

    # find position of largest number
    maxpos = np.argmax(battery)
    maxval = battery[maxpos]

    # if this is at the end of the array, look for second largest left of it
    if maxpos == len(battery)-1:
        # look to left
        secondlargest = battery[np.argmax(battery[:maxpos])]
        joltage = secondlargest*10 + maxval
    else:
        # look to right
        secondlargest = battery[maxpos+1:][np.argmax(battery[maxpos+1:])]
        joltage = maxval*10 + secondlargest
    # print(joltage)

    joltages += [joltage]

print(f'part1: {sum(joltages)=}')


#%% part 2

length = 12
joltages = []

for battery in matrix:
    # assume indices
    idx = np.arange(len(battery)-length, len(battery))

    # go through each index and try to find better position to left of it

    # jumps start for the first position

    prev_pos = -1

    for i in range(length):
        print(battery[idx])
        pos = idx[i]
        if prev_pos+1==pos:
            prev_pos = idx[i]
            continue
        curr_num = battery[pos]
        left_pos = np.argmax(battery[prev_pos+1:pos])+prev_pos+1
        left_num = battery[left_pos]
        if left_num >= curr_num:
            idx[i] = left_pos
        prev_pos = idx[i]

    joltage = int(''.join([str(x) for x in battery[idx]]))
    print(joltage)

    joltages += [joltage]

print(f'part2: {sum(joltages)=}')
# 168671466140389 too low
