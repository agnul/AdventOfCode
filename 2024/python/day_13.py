#!/usr/bin/env python3
import re

from pathlib import Path

TEST_INPUT = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

def parse_input(data):
    eqs = []
    for eq in data.split('\n\n'):
        lines = eq.splitlines()
        a1, a2 = [int(_) for _ in re.findall(r'\d+', lines[0])]
        b1, b2 = [int(_) for _ in re.findall(r'\d+', lines[1])]
        c1, c2 = [int(_) for _ in re.findall(r'\d+', lines[2])]
        eqs.append([[a1, b1], [a2, b2], [c1, c2]])
    return eqs

def solve(eq):
    a1, b1 = eq[0]
    a2, b2 = eq[1]
    c1, c2 = eq[2]

    det = a1 * b2 - b1 * a2
    if det == 0:
        return None

    a, ra = divmod(c1 * b2 - b1 * c2, det)
    b, rb = divmod(a1 * c2 - c1 * a2, det)

    return (a, b) if ra == 0 and rb == 0 else None


def part_1(eqs):
    return sum(a * 3 + b for a, b in [solve(eq) for eq in eqs if solve(eq)])

def part_2(eqs):
    for eq in eqs:
        eq[2][0] += 10000000000000
        eq[2][1] += 10000000000000
    return part_1(eqs)

if __name__ == '__main__':
    test_data = parse_input(TEST_INPUT)
    data = parse_input(Path('../inputs/day_13.txt').read_text())

    print(part_1(test_data))
    print(part_1(data))
    print(part_2(test_data))
    print(part_2(data))
