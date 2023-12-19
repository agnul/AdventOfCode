#!/usr/bin/env python3
from itertools import combinations
from pathlib import Path


TEST_UNIVERSE = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""".splitlines()

def solve(universe, expansion):
    empty_rows = [r for r, row in enumerate(universe) if all(ch == '.' for ch in row)]
    empty_cols = [c for c, col in enumerate(zip(*universe)) if all(ch == '.' for ch in col)]
    galaxies = [(r, c) for r, row in enumerate(universe) for c, ch in enumerate(row) if ch == '#']

    total = 0
    for (r1, c1), (r2, c2) in combinations(galaxies, 2):
        for r in range(min(r1, r2), max(r1, r2)):
            total += expansion if r in empty_rows else 1
        for c in range(min(c1, c2), max(c1, c2)):
            total += expansion if c in empty_cols else 1

    return total


def part_1(universe):
    return solve(universe, 2)


def part_2(universe):
    return solve(universe, 1000000)


if __name__ == '__main__':
    print(part_1(TEST_UNIVERSE))
    print(part_2(TEST_UNIVERSE))

    universe = Path('../inputs/day_11.txt').read_text().splitlines()
    print(part_1(universe))
    print(part_2(universe))
