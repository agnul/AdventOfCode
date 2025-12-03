#!/usr/bin/env python3
import re

from pathlib import Path


TEST_INPUT = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,\
1698522-1698528,446443-446449,38593856-38593862,565653-565659,\
824824821-824824827,2121212118-2121212124\
"""


def parse_input(data):
    return [tuple(map(int, r.split("-"))) for r in data.split(",")]


def part_1(data):
    return sum(
        [
            id
            for (begin, end) in data
            for id in range(begin, end + 1)
            if re.fullmatch(r"(\d+)\1", str(id))
        ]
    )


def part_2(data):
    return sum(
        [
            id
            for (begin, end) in data
            for id in range(begin, end + 1)
            if re.fullmatch(r"(\d+)\1+", str(id))
        ]
    )


if __name__ == "__main__":
    test_data = parse_input(TEST_INPUT)
    data = parse_input(Path("../inputs/day_02.txt").read_text())
    print(part_1(test_data))
    print(part_1(data))
    print(part_2(test_data))
    print(part_2(data))
