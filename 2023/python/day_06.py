#!/usr/bin/env python3
from functools import partial
from math import ceil, floor, sqrt

import re

TEST_DATA = """Time:      7  15   30
Distance:  9  40  200
"""

REAL_DATA = """Time:        46     82     84     79
Distance:   347   1522   1406   1471
"""


def collapse(data):
    return data.replace(' ', '')


def solve(data):
    times, distances = data.splitlines()
    times = [int(n) for n in re.findall(r'\d+', times)]
    distances = [int(n) for n in re.findall(r'\d+', distances)]

    res = 1
    for time, distance in zip(times, distances):
        # lambdas cause pylint to complain,
        # see: https://stackoverflow.com/q/25314547/6069
        # winning = lambda r: r > distances[i]
        # run = lambda j, t = t: j * (t - j)
        winning = partial(lambda d, r: r > d, distance)
        run  = partial(lambda t, j: j * (t - j), time)

        races = [run(j) for j in range(time + 1)]
        winners = list(filter(winning, races))

        res *= len(winners)

    return res


def solve_fast(data):
    times, distances = data.splitlines()
    times = [int(n) for n in re.findall(r'\d+', times)]
    distances = [int(n) for n in re.findall(r'\d+', distances)]

    res = 1
    for time, distance in zip(times, distances):

        delta = sqrt(time**2 - 4*distance)
        x_min, x_max = (time - delta) / 2, (time + delta) / 2
        res *= (ceil(x_max) - floor(x_min) - 1)

    return res


def part_1(data):
    return solve_fast(data)


def part_2(data):
    return solve_fast(collapse(data))


if __name__ == '__main__':
    print(part_1(TEST_DATA))
    print(part_2(TEST_DATA))

    print(part_1(REAL_DATA))
    print(part_2(REAL_DATA))
