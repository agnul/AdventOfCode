#!/usr/bin/env python3
from pathlib import Path

import re


def parse_input(data):
    cards = []
    for line in data.splitlines():
        card, numbers, winners = re.split(r'[:|]', line)
        cards.append({
            'card': int(card[5:]),
            'numbers': set(re.findall(r'\d+', numbers)),
            'winners': set(re.findall(r'\d+', winners))
        })
    return cards


def part_1(cards):
    sum = 0
    for c in cards:
        winning = c['numbers'].intersection(c['winners'])
        sum += 2 ** (len(winning) - 1) if winning else 0
    return sum


def part_2(cards):
    counts = [1] * len(cards)
    for i, c in enumerate(cards):
        cards_won = len(c['numbers'].intersection(c['winners']))
        for w in range(1, cards_won + 1):
            counts[i + w] += counts[i]
    return sum(counts)


if __name__ == '__main__':
    test_data = parse_input(Path('../inputs/day_04_test.txt').read_text())
    real_data = parse_input(Path('../inputs/day_04.txt').read_text())

    print(part_1(test_data))
    print(part_1(real_data))

    print(part_2(test_data))
    print(part_2(real_data))
