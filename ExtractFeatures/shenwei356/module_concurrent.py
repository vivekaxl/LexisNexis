#!/usr/bin/env python3

import multiprocessing
from multiprocessing import Pool


def f(x):
    print(x)
    return pow(x, 6)

with Pool(processes=multiprocessing.cpu_count()) as pool:
    print(pool.map(f, range(1, 100)))