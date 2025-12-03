#!/usr/bin/env python3
from pathlib import Path


TEST_INPUT = """987654321111111
811111111111119
234234234234278
818181911112111
"""


def parse_input(input):
    return input.splitlines()


def max_with_index(values):
    idx = max(range(len(values)), key=values.__getitem__)
    return values[idx], idx


def max_jolts(pack, count):
    left, right = 0, len(pack)
    active = []
    for remaining in range(count, 0, -1):
        m, i = max_with_index(pack[left : right - remaining + 1])
        active.append(m)
        left += i + 1
    return int("".join(active))


def part_1(packs):
    return sum(max_jolts(p, 2) for p in packs)


def part_2(packs):
    return sum(max_jolts(p, 12) for p in packs)


if __name__ == "__main__":
    test_data = parse_input(TEST_INPUT)
    data = parse_input(Path("../inputs/day_03.txt").read_text())
    print(part_1(test_data))
    print(part_1(data))
    print(part_2(test_data))
    print(part_2(data))
