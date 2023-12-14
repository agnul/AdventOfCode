#!/usr/bin/env python3
from math import gcd
from functools import reduce
from itertools import cycle
from pathlib import Path

import re


TEST_DATA = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

TEST_DATA_2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

TEST_DATA_3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


def parse_input(data):
    directions, maps = data.split("\n\n")
    network  = {}
    for m in maps.splitlines():
        key, left, right = re.match(r'^(.*) = \((.*), (.*)\)$', m).groups()
        network[key] = (left, right)
    return directions, network


def walk(directions, maps):
    pos = 'AAA'
    for steps, dir in enumerate(cycle(directions)):
        if pos == 'ZZZ':
            break
        pos = maps[pos][0 if dir == 'L' else 1]
    return steps


def lcm(a, b):
    return a * b // gcd(a, b)


def walk_n(directions, maps):
    posns = [m for m in maps if m.endswith('A')]
    steps = [0] * len(posns)
    for dir in cycle(directions):
        if all(p.endswith('Z') for p in posns):
            break;
        for j, pos in enumerate(posns):
            if pos.endswith('Z'):
                continue
            posns[j] = maps[pos][0 if dir == 'L' else 1]
            steps[j] += 1
    return reduce(lcm, steps, 1)


def part_1(directions, maps):
    return walk(directions, maps)


def part_2(directions, maps):
    return walk_n(directions, maps)


if __name__ == '__main__':
    print(part_1(*parse_input(TEST_DATA)))
    print(part_1(*parse_input(TEST_DATA_2)))

    real_data = Path('../inputs/day_08.txt').read_text()

    print(part_1(*parse_input(real_data)))

    print(part_2(*parse_input(TEST_DATA_3)))
    print(part_2(*parse_input(real_data)))
