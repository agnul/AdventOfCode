#!/usr/bin/env python3
from pathlib import Path


TEST_GRID = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""

TEST_GRID_2 = """..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
"""

PIPE_EXITS = {
    'S': [(-1, 0), (1, 0), (0, -1), (0, 1)],
    '|': [(-1, 0), (1, 0)],
    '-': [(0, -1), (0, 1)],
    'L': [(-1, 0), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    '7': [(1, 0), (0, -1)],
    'F': [(1, 0), (0, 1)]
}


def pipe_exits(grid, r, c):
    cur = grid[r][c]
    for dr, dc in PIPE_EXITS[cur]:
        xr = r + dr
        xc = c + dc
        if 0 <= xr < len(grid) and 0 <= xc < len(grid[0]) and grid[xr][xc] in 'S|-LJ7F':
            yield xr, xc


def find_entry(grid):
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == 'S':
                return r, c
    return None


def find_loop(grid):
    start_r, start_c = find_entry(grid)

    loop = [(start_r, start_c)]

    closed_loop = False
    while not closed_loop:
        cur_r, cur_c = loop[-1]
        for r, c in pipe_exits(grid, cur_r, cur_c):
            if len(loop) < 2:
                loop.append((r, c))
                break
            elif loop[-2] != (r, c):
                loop.append((r, c))
                break
        closed_loop = (loop[-1] == (start_r, start_c))
    return loop


def part_1(grid):
    return len(find_loop(grid)) // 2


def part_2(grid):
    loop = find_loop(grid)
    vertexes = len(loop)

    area = 0
    for (x1, y1), (x2, y2) in zip(loop, loop[1:]):
        area += x1 * y2 - y1 * x2
    
    area = abs(area) // 2
    return area + 1 - vertexes // 2



if __name__ == '__main__':
    print(part_1(TEST_GRID.splitlines()))
    print(part_1(TEST_GRID_2.splitlines()))
    print(part_2(TEST_GRID_2.splitlines()))

    real_grid = Path('../inputs/day_10.txt').read_text()
    print(part_1(real_grid.splitlines()))
    print(part_2(real_grid.splitlines()))
