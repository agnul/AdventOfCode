#!/usr/bin/env python3
from functools import reduce
from pathlib import Path


TEST_DATA = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

def differences(line):
    nums = line
    deltas = [line]
    while any(nums):
        nums = [b - a for a, b in zip(nums, nums[1:])]
        deltas.append(nums)
    return deltas


def derive_last(line):
    return sum(d[-1] for d in differences(line)[::-1])


def derive_first(line):
    deltas = [d[0] for d in differences(line)]
    return reduce(lambda acc, d: -1 * acc + d, deltas[::-1])


def part_1(lines):
    return sum(derive_last(line) for line in lines)


def part_2(lines):
    return sum(derive_first(line) for line in lines)


if __name__ == '__main__':
    test_report = [[int(n) for n in line.split()] for line in TEST_DATA.splitlines()]
    print(part_1(test_report))
    print(part_2(test_report))

    data = Path('../inputs/day_09.txt').read_text()
    report = [[int(n) for n in line.split()] for line in data.splitlines()]
    print(part_1(report))
    print(part_2(report))
