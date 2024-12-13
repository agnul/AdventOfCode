#!/usr/bin/env python3
from itertools import batched
from pathlib import Path

TEST_INPUT = "2333133121414131402"

def parse_input(data):
    disk = []
    for id, pair in enumerate(batched(data, 2)):
        sz = pair[0]
        free = pair[1] if len(pair) == 2 else 0
        disk += [id] * int(sz) + ['.'] * int(free)
    return disk

def part_1(data):
    i, j, disk = 0, len(data) - 1, []
    while i <= j:
        if data[i] != '.':
            disk.append(data[i])
            i += 1
        elif data[j] != '.':
            disk.append(data[j])
            i += 1
            j -= 1
        else:
            j -= 1
    total = len([d for d in data if d != '.'])
    print(total, len(disk), i, j)
    return sum(i * int(n) for i, n in enumerate(disk))

def part_2(data):
    pass


if __name__ == '__main__':
    test_data = parse_input(TEST_INPUT)
    data = parse_input(Path('../inputs/day_09.txt').read_text().rstrip())

    print(part_1(test_data))
    print(part_1(data))
    print(part_2(test_data))
    print(part_2(data))
