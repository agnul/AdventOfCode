#!/usr/bin/env python3
from collections import Counter
from pathlib import Path

TEST_INPUT = """3   4
4   3
2   5
1   3
3   9
3   3
"""

def parse_input(data):
    numbers = [int(n) for n in data.split()]
    left = numbers[0::2]
    right = numbers[1::2]
    return left, right

def part_1(left, right):
    left, right = sorted(left), sorted(right)
    return sum(abs(r - l) for l, r in zip(left, right))

def part_2(left, right):
    counts = Counter(right)
    return sum (l * counts[l] for l in left)


if __name__ == '__main__':
    test_data = parse_input(TEST_INPUT)
    data = parse_input(Path('../inputs/day_01.txt').read_text())
    print(part_1(*test_data))
    print(part_1(*data))
    print(part_2(*test_data))
    print(part_2(*data))
