#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 08:02:16 2025

@author: simon
"""

from tqdm import tqdm
from aoc import get_input, get_lines
from tqdm import tqdm

x = get_input(2)

x2 = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"


#%% part 1
# "There are clever solutions, but this ain't it"

ranges = x.split(',')

invalid = []

for r in tqdm(ranges):
    start, stop = r.split('-')
    for n in range(int(start), int(stop)):
        n = str(n)

        if n[:len(n)//2]==n[len(n)//2:]:
            invalid += [int(n)]

print(sum(invalid))


#%% part 2
# "Why use brain power when you can brute force faster"

from more_itertools import chunked
ranges = x.split(',')

invalid = []

for r in tqdm(ranges):
    start, stop = r.split('-')
    for n in range(int(start), int(stop)+1):
        n = str(n)
        for chunksize in range(1, len(n)//2+1):
            chunks = [''.join(c) for c in chunked(n, chunksize)]
            if len(set(chunks))==1:
                if int(n) in invalid: continue
                invalid += [int(n)]


print(sum(invalid))

# 16182750391 too low
# 54340905147 too high
