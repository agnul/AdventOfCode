#!/usr/bin/env python3
from pathlib import Path
import re

TEST_INPUT = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

TEST_INPUT_2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

DIGITS = {
    'one':   1, 'two':   2, 'three': 3,
    'four':  4, 'five':  5, 'six':   6,
    'seven': 7, 'eight': 8, 'nine':  9
}

def to_int(s):
    if s.isdigit():
        return int(s)
    return DIGITS[s]

def part_1(data):
    sum = 0
    for line in data.rstrip().split('\n'):
        first = re.search(r'\d', line).group()
        last = re.search(r'\d', line[::-1]).group()
        sum += int(first) * 10 + int(last)
    return sum

def part_2(data):
    sum = 0
    regex = '|'.join(DIGITS.keys())
    xereg = regex[::-1]

    for line in data.rstrip().split('\n'):
        first = re.search(regex + r'|\d', line).group()
        last = re.search(xereg + r'|\d', line[::-1]).group()[::-1]
        sum += to_int(first) * 10 + to_int(last)
    return sum


if __name__ == '__main__':
    print(part_1(TEST_INPUT))
    print(part_1(Path('../inputs/day_01.txt').read_text()))
    print(part_2(TEST_INPUT_2))
    print(part_2(Path('../inputs/day_01.txt').read_text()))
