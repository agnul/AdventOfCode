#!/usr/bin/env python3
from pathlib import Path

TEST_INPUT = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

def parse_input(data):
    return [[int(n) for n in l.split()] for l in data.splitlines()]

def increasing(report):
    return [(a < b and b - a <= 3) for a, b in zip(report, report[1:])]

def decreasing(report):
    return [(a > b and a - b <= 3) for a, b in zip(report, report[1:])]

def is_safe(report):
    return all(increasing(report)) or all(decreasing(report))

def can_apply_dampener(report):
    return any(is_safe(report[0:i] + report[i+1:]) for i in range(len(report)))

def part_1(reports):
    return len([r for r in reports if is_safe(r)])

def part_2(reports):
    return len([r for r in reports if is_safe(r) or can_apply_dampener(r)])


if __name__ == '__main__':
    test_reports = parse_input(TEST_INPUT)
    reports = parse_input(Path('../inputs/day_02.txt').read_text())
    print(test_reports)
    print(part_1(test_reports))
    print(part_1(reports))
    print(part_2(test_reports))
    print(part_2(reports))
