#!/usr/bin/env python3
from pathlib import Path

import re


def parse(grid):
    parts = []
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if not (char.isdigit() or char == '.'):
                parts.append((char, find_part_numbers(grid, i, j)))
    return parts


def find_part_numbers(grid, row, col):
    res = []
    rows = len(grid)
    for i in [max(0, row - 1), row, min(rows, row + 1)]:
        for left, right in map(re.Match.span, re.finditer(r'\d+', grid[i])):
            if left - 1 <= col <= right:
                res.append(int(grid[i][left:right]))
    return res


def part_1(data):
    return sum((sum(ns) for _, ns in data))


def part_2(data):
    gears = filter(lambda d: d[0] == '*' and len(d[1]) == 2, data)
    return sum(a * b for _, [a, b] in gears)


if __name__ == '__main__':
    test_grid = parse([line.rstrip() for line in Path(
        '../inputs/day_03_test.txt').read_text().splitlines()])
    real_grid = parse([line.rstrip() for line in Path(
        '../inputs/day_03.txt').read_text().splitlines()])

    print(part_1(test_grid))
    print(part_2(test_grid))

    print(part_1(real_grid))
    print(part_2(real_grid))
