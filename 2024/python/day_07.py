#!/usr/bin/env python3
from pathlib import Path

TEST_INPUT = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

def parse_input(data):
    res = []
    for line in data.splitlines():
        goal, numbers = line.split(':')
        res.append([int(goal), [int(n) for n in numbers.split()]])
    return res

def cat(n1, n2):
    return int(str(n1) + str(n2))

def sat(goal, current, numbers, pt2=False):
    if len(numbers) == 1:
        if goal == current + numbers[0]: return True
        if goal == current * numbers[0]: return True
        return pt2 and goal == cat(current, numbers[0])

    if sat(goal, current + numbers[0], numbers[1:], pt2): return True
    if sat(goal, current * numbers[0], numbers[1:], pt2): return True
    return pt2 and sat(goal, cat(current, numbers[0]), numbers[1:], pt2)

def part_1(data):
    return sum(goal for goal, numbers in data if sat(goal, numbers[0], numbers[1:]))

def part_2(data):
    return sum(goal for goal, numbers in data if sat(goal, numbers[0], numbers[1:], True))


if __name__ == '__main__':
    test_data = parse_input(TEST_INPUT)
    data = parse_input(Path('../inputs/day_07.txt').read_text())

    print(part_1(test_data))
    print(part_1(data))
    print(part_2(test_data))
    print(part_2(data))
