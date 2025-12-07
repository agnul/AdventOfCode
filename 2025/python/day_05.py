#!/usr/bin/env python3
from operator import itemgetter
from pathlib import Path


TEST_INPUT = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""


def parse_input(input):
    ranges, ids = input.split("\n\n")
    fresh = [tuple(map(int, r.split("-"))) for r in ranges.splitlines()]
    have = [int(id) for id in ids.splitlines()]

    return sorted(fresh, key=itemgetter(0)), have


def merge_ranges(ranges):
    merged = [ranges[0]]
    for l, r in ranges[1:]:
        cur_min, cur_max = merged[-1]
        if l <= cur_max:
            merged[-1] = (cur_min, max(r, cur_max))
        elif l > cur_max:
            merged.append((l, r))
    return merged


def part_1(fresh, have):
    return len(
        [id for id in have if any([min <= id <= max for min, max in fresh])]
    )


def part_2(fresh):
    return sum(max - min + 1 for min, max in merge_ranges(fresh))


if __name__ == "__main__":
    test_data = parse_input(TEST_INPUT)
    data = parse_input(Path("../inputs/day_05.txt").read_text())
    print(part_1(*test_data))
    print(part_1(*data))
    print(part_2(test_data[0]))
    print(part_2(data[0]))
