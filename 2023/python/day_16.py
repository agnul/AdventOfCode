#!/usr/bin/env python3
from collections import deque
from pathlib import Path


TEST_DATA = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
""".splitlines()

DELTAS = {
    'U': (-1, 0), 'D': (1, 0), 'R': (0, 1), 'L': (0, -1)
}

BEAM_DESTINATIONS = {
    '.':  { 'R': 'R', 'L': 'L', 'U': 'U', 'D': 'D' },
    '|':  { 'R': 'UD', 'L': 'UD', 'U': 'U', 'D': 'D' },
    '-':  { 'R': 'R', 'L': 'L', 'U': 'LR', 'D': 'LR' },
    '\\': { 'R': 'D', 'L': 'U', 'U': 'L', 'D': 'R' },
    '/':  { 'R': 'U', 'L': 'D', 'U': 'R', 'D': 'L' },
}


def traverse(grid, height, witdth, start=(0, 0, 'R')):
    visited = set()
    to_visit = deque()
    to_visit.append(start)
    while to_visit:
        row, col, direction = to_visit.popleft()
        if (row, col, direction) in visited:
            continue
        visited.add((row, col, direction))
        for dst in BEAM_DESTINATIONS[grid[row][col]][direction]:
            dr, dc = DELTAS[dst]
            if 0 <= row + dr < height and 0 <= col + dc < witdth:
                to_visit.append((row+dr, col+dc, dst))
    return len({(r, c) for r, c, _ in visited})


def part_1(grid):
    height = len(grid)
    width = len(grid[0])
    return traverse(grid, height, width)


def part_2(grid):
    height = len(grid)
    width = len(grid[0])
    max_energy = 0
    for r in range(height):
        max_energy = max(max_energy, traverse(grid, height, width, (r, 0, 'R')))
        max_energy = max(max_energy, traverse(grid, height, width, (r, width - 1, 'L')))
    for c in range(width):
        max_energy = max(max_energy, traverse(grid, height, width, (0, c, 'D')))
        max_energy = max(max_energy, traverse(grid, height, width, (height-1, c, 'U')))
    return max_energy


if __name__ == '__main__':
    print(part_1(TEST_DATA))
    print(part_2(TEST_DATA))

    data = Path('../inputs/day_16.txt').read_text().splitlines()
    print(part_1(data))
    print(part_2(data))
