#!/usr/bin/env python3
from pathlib import Path

TEST_DATA = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


def transpose(grid):
    return tuple(''.join(column) for column in zip(*grid))


def roll_left(rocks):
    return ''.join(sorted(rocks, reverse=True))


def roll_right(rocks):
    return ''.join(sorted(rocks))


def tilt_north(dish):
    cols = transpose(dish)
    tilted = tuple('#'.join([roll_left(span) for span in c.split('#')]) for c in cols)
    return transpose(tilted)


def tilt_west(dish):
    return tuple('#'.join([roll_left(span) for span in row.split('#')]) for row in dish)


def tilt_south(dish):
    cols = transpose(dish)
    tilted = tuple('#'.join([roll_right(span) for span in c.split('#')]) for c in cols)
    return transpose(tilted)


def tilt_east(dish):
    return tuple('#'.join([roll_right(span) for span in row.split('#')]) for row in dish)


def spin(dish):
    dish = tilt_north(dish)
    dish = tilt_west(dish)
    dish = tilt_south(dish)
    dish = tilt_east(dish)
    return dish


def _spin(dish):
    for _ in range(4):
        dish = tuple(''.join(c) for c in zip(*dish))
        dish = tuple('#'.join([roll_left(span) for span in row.split('#')]) for row in dish)
        dish = tuple(t[::-1] for t in dish)
    return dish


def part_1(dish):
    return sum(line.count('O') * (len(dish) - i) for i, line in enumerate(tilt_north(dish)))


def part_2(dish):
    seen = {dish}
    steps = [dish]

    iterations = 0
    while True:
        iterations += 1
        dish = spin(dish)
        if dish in seen:
            break
        seen.add(dish)
        steps.append(dish)

    loop_start = steps.index(dish)
    loop_size = iterations - loop_start
    result = steps[loop_start + (1000000000 - loop_start) % loop_size]

    return sum(line.count('O') * (len(result) - i) for i, line in enumerate(result))


if __name__ == '__main__':
    print(part_1(tuple(TEST_DATA.splitlines())))
    print(part_2(tuple(TEST_DATA.splitlines())))

    data = Path('../inputs/day_14.txt').read_text()
    print(part_1(tuple(data.splitlines())))
    print(part_2(tuple(data.splitlines())))
