#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 11:21:29 2025

@author: simon
"""
from tqdm import tqdm
from aoc import get_input, get_lines

lines = get_lines(1)


lines2 ='''L68
L30
R48
L5
R60
L55
L1
L99
R14
L82'''.split()


#%% part 1
pos = 50

count = 0

for line in tqdm(lines):
    if line.startswith('R'):
        pos += int(line[1:])
    elif line.startswith('L'):
        pos -= int(line[1:])
    else:
        raise Exception

    pos %= 100

    if pos == 0:
        count += 1

print(f'\n{count=}')


#%% part 2

pos = 50

count = 0

for line in lines:
    d, *mov = line

    mov = int(''.join(mov))

    plus = d=='R'

    # ok let's do this the stupid way with a loop

    for _ in range(mov):
        if plus:
            pos += 1
        else:
            pos -=1

        # reset if we're over the bounds
        if pos>99:
            pos = 0
        elif pos<0:
            pos = 99

        # every time we pass, increase counter
        if pos==0:
            count += 1


print(f'\n{count=}')

# 6612 too low
# 6511 too low
