#!/usr/bin/env python3
from itertools import batched
from pathlib import Path


TEST_INPUT = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""


class Grid:
    def __init__(self, lines):
        self.lines = lines
        self.rows = len(lines)
        self.cols = len(lines[0])

    def at(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.lines[r][c]
        else:
            raise ValueError(f"Invalid grid position {r}, {c}.")

    def by_row(self):
        for r in range(self.rows):
            for c in range(self.cols):
                yield r, c

    def neighbours(self, r, c):
        deltas = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        for dr, dc in deltas:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                yield self.at(nr, nc)


def parse_input(input):
    return input.splitlines()


def part_1(floor):
    f = Grid(floor)
    cnt = 0
    for r, c in f.by_row():
        n = len([t for t in f.neighbours(r, c) if t == "@"])
        cnt += 1 if f.at(r, c) != "." and n < 4 else 0
    return cnt


def part_2(floor):
    f = Grid(floor)

    removed = 0
    while True:
        new_floor = ""
        removed_this_round = 0

        for r, c in f.by_row():
            n = len([t for t in f.neighbours(r, c) if t == "@"])
            can_remove = f.at(r, c) != "." and n < 4
            if can_remove:
                removed_this_round += 1
                new_floor += "."
            else:
                new_floor += f.at(r, c)

        f = Grid(list(batched(new_floor, f.cols)))
        removed += removed_this_round

        if removed_this_round == 0:
            break

    return removed


if __name__ == "__main__":
    test_data = parse_input(TEST_INPUT)
    data = parse_input(Path("../inputs/day_04.txt").read_text())
    print(part_1(test_data))
    print(part_1(data))
    print(part_2(test_data))
    print(part_2(data))
