#!/usr/bin/env python3
import re

from pathlib import Path

TEST_INPUT = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
TEST_INPUT_2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

def part_1(mem):
    res = 0
    for m in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)", mem):
        res += int(m.group(1)) * int(m.group(2))
    return res

def part_2(mem):
    mul, res = True, 0
    for m in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))", mem):
        if m.group(3) == 'do()':
            mul = True
        elif m.group(4) == "don't()":
            mul = False
        elif mul:
            l, r = int(m.group(1)), int(m.group(2))
            res += l * r
    return res


if __name__ == '__main__':
    memory = Path('../inputs/day_03.txt').read_text()
    print(part_1(TEST_INPUT))
    print(part_1(memory))
    print(part_2(TEST_INPUT_2))
    print(part_2(memory))
