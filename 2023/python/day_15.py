#!/usr/bin/env python3
from functools import reduce
from pathlib import Path

import re

def HASH(step):
    return reduce(lambda acc, c: ((acc + ord(c)) * 17) % 256, step, 0)


def add_lens(box, label, focal_length):
    box[label] = focal_length


def remove_lens(box, label):
    if label in box:
        del box[label]


def part_1(init_sequence):
    return sum(HASH(s) for s in init_sequence.split(','))


def part_2(init_sequence):
    boxes = [dict() for _ in range(256)]
    for step in init_sequence.split(','):
        label, focal_length = re.split(r'[-=]', step)
        if focal_length:
            add_lens(boxes[HASH(label)], label, int(focal_length))
        else:
            remove_lens(boxes[HASH(label)], label)
    total = 0
    for i, box in enumerate(boxes, 1):
        for j, label in enumerate(box, 1):
            total += i * j * box[label]
    return total


if __name__ == '__main__':
    TEST_DATA = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'
    print(part_1(TEST_DATA))
    print(part_2(TEST_DATA))

    data = Path('../inputs/day_15.txt').read_text()
    print(part_1(data))
    print(part_2(data))
