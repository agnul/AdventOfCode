#!/usr/bin/env python3
from pathlib import Path

TEST_DATA="""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


def is_reflection(grid, row):
    size = min(row, len(grid) - row)
    return all(grid[row-i-1] == grid[row+i] for i in range(0, size))


def is_reflection_pt2(grid, row, max_differences):
    size = min(row, len(grid) - row)
    differences = 0
    for i in range(0, size):
        differences += sum(0 if a == b else 1 for a, b in zip(grid[row-i-1], grid[row+i]))
    return differences == max_differences


def part_1(data):
    total = 0
    for grid in data:
        rows = grid.splitlines()
        for r in range(1, len(rows)):
            total += 100 * r if is_reflection(rows, r) else 0

        cols = [''.join(c) for c in zip(*rows)]
        for c in range(1, len(cols)):
            total += c if is_reflection(cols, c) else 0
    return total


def part_2(data):
    total = 0
    for grid in data:
        rows = grid.splitlines()
        for r in range(1, len(rows)):
            total += 100 * r if is_reflection_pt2(rows, r, 1) else 0

        cols = [''.join(c) for c in zip(*rows)]
        for c in range(1, len(cols)):
            total += c if is_reflection_pt2(cols, c, 1) else 0
    return total


if __name__ == '__main__':
    test_grids = TEST_DATA.split('\n\n')
    print(part_1(test_grids))
    print(part_2(test_grids))

    grids = Path('../inputs/day_13.txt').read_text().split('\n\n')
    print(part_1(grids))
    print(part_2(grids))
