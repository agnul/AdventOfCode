#!/usr/bin/env python3
import re

from collections import defaultdict, deque
from pathlib import Path

TEST_INPUT="""1
10
100
2024
"""

TEST_INPUT_2="""1
2
3
2024
"""


def evolve(initial, rounds=1):
    res = initial
    for _ in range(rounds):
        res = ((res <<  6) ^ res) & 0xffffff
        res = ((res >>  5) ^ res) & 0xffffff
        res = ((res << 11) ^ res) & 0xffffff
    return res


def part_1(secrets):
    return sum(evolve(s, 2000) for s in secrets)


def part_2(secrets):
    sales = defaultdict(int)
    for s in secrets:
        seen = set()
        window = deque([s], maxlen=5)
        for _ in range(1999):
            window.append(evolve(window[-1]))
            if len(window) < 5:
                continue
            diffs = tuple(window[i] % 10 - window[i-1] % 10 for i in range(1, 5))
            if diffs in seen:
                continue
            seen.add(diffs)
            sales[diffs] += window[-1] % 10
    return max(sales.values())


if __name__ == '__main__':
    test_secrets = [int(_) for _ in re.findall(r'\d+', TEST_INPUT)]
    real_secrets = [int(_) for _ in re.findall(r'\d+', Path('../inputs/day_22.txt').read_text())]

    print(part_1(test_secrets))
    print(part_1(real_secrets))

    print(part_2([1, 2, 3, 2024]))
    print(part_2(real_secrets))
