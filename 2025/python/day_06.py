#!/usr/bin/env python3
from math import prod
from pathlib import Path


TEST_INPUT = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
"""


def parse_input(input):
    lines = input.splitlines()
    operations = lines[-1].split()

    longest = max(len(l) for l in lines[:-1])
    lines = [l.ljust(longest + 1) for l in lines[:-1]]
    return lines, operations


def columns(lines):
    columns = []
    col_acc = []
    for c in range(len(lines[0])):
        num = "".join(lines[r][c] for r in range(len(lines)))
        if num.strip():
            col_acc.append(int(num))
        else:
            columns.append(col_acc)
            col_acc = []
    return columns


def part_1(lines, operations):
    args = [[int(n) for n in a.split()] for a in lines]

    res = 0
    for i, op in enumerate(operations):
        if op == "+":
            res += sum(args[r][i] for r in range(len(args)))
        elif op == "*":
            res += prod(args[r][i] for r in range(len(args)))
    return res


def part_2(lines, operations):
    args = columns(lines)

    res = 0
    for i, op in enumerate(operations):
        if op == "+":
            res += sum(args[i])
        elif op == "*":
            res += prod(args[i])
    return res


if __name__ == "__main__":
    test_data = parse_input(TEST_INPUT)
    data = parse_input(Path("../inputs/day_06.txt").read_text())
    print(part_1(*test_data))
    print(part_1(*data))
    print(part_2(*test_data))
    print(part_2(*data))
