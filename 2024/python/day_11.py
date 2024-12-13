#!/usr/bin/env python3
from pathlib import Path

TEST_INPUT = "125 17"

def parse_input(data):
    return [int(_) for _ in data.split()]

def blink(cache, stone, times):
    if (stone, times) in cache:
        return cache[(stone, times)]

    if times == 0:
        return 1

    s_stone = str(stone)
    s_len = len(s_stone)
    if stone == 0:
        cache[(stone, times)] = blink(cache, 1, times - 1)
    elif s_len % 2 == 0:
        left = int(s_stone[:s_len//2])
        right = int(s_stone[s_len//2:])
        cache[(stone, times)] = blink(cache, left, times - 1) + blink(cache, right, times - 1)
    else:
        cache[(stone, times)] = blink(cache, stone * 2024, times - 1)

    return cache[(stone, times)]


def part_1(data):
    cache = {}
    return sum(blink(cache, stone, 25) for stone in data)

def part_2(data):
    cache = {}
    return sum(blink(cache, stone, 75) for stone in data)

if __name__ == '__main__':
    test_data = parse_input(TEST_INPUT)
    data = parse_input(Path('../inputs/day_11.txt').read_text())

    print(part_1(test_data))
    print(part_1(data))
    print(part_2(test_data))
    print(part_2(data))
