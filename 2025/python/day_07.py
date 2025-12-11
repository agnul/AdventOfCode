#!/usr/bin/env python3
from collections import defaultdict
from pathlib import Path


TEST_INPUT = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""


def parse_input(input):
    rows = input.splitlines()
    beams = {(0, rows[0].index("S"))}
    return beams, rows[1:]


def part_1(beams, rows):
    splits = 0
    for r, row in enumerate(rows):
        new_beams = set()
        for c, ch in enumerate(row):
            if (r, c) not in beams:
                continue
            if ch == "^":
                splits += 1
                new_beams.add((r + 1, c - 1))
                new_beams.add((r + 1, c + 1))
            else:
                new_beams.add((r + 1, c))
        beams = new_beams.copy()
    return splits


def part_2(start, rows):
    beams = {b: 1 for b in start}
    for r, row in enumerate(rows):
        new_beams = defaultdict(int)
        for c, ch in enumerate(row):
            if (r, c) not in beams:
                continue
            if ch == "^":
                new_beams[(r + 1, c - 1)] += beams[(r, c)]
                new_beams[(r + 1, c + 1)] += beams[(r, c)]
            else:
                new_beams[r + 1, c] += beams[(r, c)]
        beams = new_beams
    return sum(beams.values())


if __name__ == "__main__":
    test_data = parse_input(TEST_INPUT)
    data = parse_input(Path("../inputs/day_07.txt").read_text())
    print(part_1(*test_data))
    print(part_1(*data))
    print(part_2(*test_data))
    print(part_2(*data))
