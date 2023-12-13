#!/usr/bin/env python
from collections import Counter
from pathlib import Path


TEST_DATA = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""".splitlines()


def hand_type(hand_and_bid):
    return ''.join(map(str, sorted(Counter(hand_and_bid[:5]).values(), reverse=True)))


def hand_type_with_jokers(hand_and_bid):
    hand = hand_and_bid[:5].replace('J', '')
    jokers = 5 - len(hand)
    counts = sorted(Counter(hand).values(), reverse=True)
    if jokers < 5:
        counts[0] += jokers
    else:
        counts = [5]
    return ''.join(map(str, counts))


def hand_strength(hand, hand_type_fn, face_values):
    return hand_type_fn(hand) + ''.join(face_values[c] for c in hand)


def solve(data, card_strength, face_values):
    key_fn = lambda line: hand_strength(line[:5], card_strength, face_values)
    winnings = 0
    for i, line in enumerate(sorted(data, key=key_fn), start=1):
        winnings += i * int(line[6:])
    return winnings


def part_1(data):
    face_values = dict(zip('23456789TJQKA', 'ABCDEFGHIJKLM'))
    return solve(data, hand_type, face_values)


def part_2(data):
    face_values = dict(zip('J23456789TQKA', 'ABCDEFGHIJKLM'))
    return solve(data, hand_type_with_jokers, face_values)


if __name__ == '__main__':
    real_data = Path('../inputs/day_07.txt').read_text().splitlines()

    print(part_1(TEST_DATA))
    print(part_1(real_data))

    print(part_2(TEST_DATA))
    print(part_2(real_data))
