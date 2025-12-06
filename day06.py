#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  6 07:36:02 2025

@author: simon
"""

import numpy as np
from tqdm import tqdm
from aoc import get_input, get_lines, get_matrix, lines2matrix, input2matrix

content = get_input(6)

content2 = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """


# parse it into useable form
content, operators = content.rsplit('\n', 1)
operators = [x.strip() for x in operators.split(' ') if x]

#%% part 1

# I've put this into part1 as it is mostly about the parsing not the compute
lines = content.split('\n')
lines = [[int(x) for x in line.split(' ') if x!=''] for line in lines]
matrix = np.array(lines)

summed = 0

for i, op in enumerate(operators):
    if op=='*':
        summed += np.prod(matrix[:, i])
    elif op=='+':
        summed += np.sum(matrix[:, i])
    else:
        raise Exception

print(f'{summed=}')

#%% part 2

import more_itertools

lines = [[x for x in line] for line in content.split('\n')]
# next pad lines to be same length
maxlen = max([len(line) for line in lines])
lines = [line + [' ']*(maxlen - len(line)) for line in lines]

matrix = np.array(lines).T
numbers = [int(''.join(x)) if ''.join(x).strip() else '' for x in matrix]

# some operators have 2 other 4 numbers. luckily, the split_at function
# can help here to segment the lists easily
numbers = list(more_itertools.split_at(numbers, lambda x: x==''))

summed = 0

for i, (op, nums) in enumerate(zip(operators, numbers)):
    print(op, nums)
    if op=='*':
        summed += np.prod(nums)
    elif op=='+':
        summed += np.sum(nums)
    else:
        raise Exception

print(f'{summed=}')
