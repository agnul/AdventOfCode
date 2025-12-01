#!/usr/bin/env python3
from functools import reduce
from pathlib import Path


TEST_INPUT = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""


def rotate(pos, direction, count):
    return (pos - count) % 100 if direction == "L" else (pos + count) % 100


def count_zeros(acc, arg):
    pos, zeros = acc
    dir, amt = arg
    new_pos = rotate(pos, dir, amt)
    return (new_pos, zeros + 1 if new_pos == 0 else zeros)


def count_clicks(acc, arg):
    pos, clicks = acc
    dir, amt = arg

    complete_turns, rem = divmod(amt, 100)
    clicks += complete_turns

    new_pos = rotate(pos, dir, rem)
    did_cross_0 = (
        new_pos == 0
        or (pos != 0 and dir == "L" and new_pos > pos)
        or (pos != 0 and dir == "R" and new_pos < pos)
    )
    return (new_pos, clicks + 1 if did_cross_0 else clicks)


def parse_input(data):
    return [(rot[0], int(rot[1:])) for rot in data.split()]


def part_1(rotations):
    _, count = reduce(count_zeros, rotations, (50, 0))
    return count


def part_2(rotations):
    _, count = reduce(count_clicks, rotations, (50, 0))
    return count


if __name__ == "__main__":
    test_data = parse_input(TEST_INPUT)
    data = parse_input(Path("../inputs/day_01.txt").read_text())
    print(part_1(test_data))
    print(part_1(data))
    print(part_2(test_data))
    print(part_2(data))
