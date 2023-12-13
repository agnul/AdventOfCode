#!/usr/bin/env python3
from pathlib import Path

import re


def parse_block(block):
    parse_line = lambda l: map(int, re.findall(r'\d+', l))

    return [tuple(t) for t in map(parse_line, block.splitlines()[1:])]


def parse_input(lines):
    blocks = lines.split('\n\n')
    seeds = list(map(int, re.findall(r'\d+', blocks[0])))

    return seeds, [parse_block(b) for b in blocks[1:]]


def translate(seed, trans):
    for dst, src, size in trans:
        if src <= seed < src + size:
            return dst + seed - src
    return seed


def translate_pt2(seed_intervals, translations):
    done = []
    while seed_intervals:
        start, count = seed_intervals.pop()
        for dst, src, size in translations:
            left = max(start, src)
            right = min(start + count, src + size)
            if left < right:
                done.append((left + (dst - src), right - left))
                if left > start:
                    seed_intervals.append((start, left - start))
                if start + count > right:
                    seed_intervals.append((right, start + count - right))
                break
        else:
            done.append((start, count))
    return done


def part_1(seeds, translations):
    soils = []
    for seed in seeds:
        for trans in translations:
            seed = translate(seed, trans)
        soils.append(seed)
    return min(soils)


def part_1b(seeds, translations):
    seed_intervals = [(s, s+1) for s in seeds]
    for trans in translations:
        seed_intervals = translate_pt2(seed_intervals, trans)
    return min(seed_intervals)[0]


def part_2(seeds, translation_blocks):
    seed_intervals = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]

    for block in translation_blocks:
        seed_intervals = translate_pt2(seed_intervals, block)
    return min(seed_intervals)[0]


if __name__ == '__main__':
    test_data = Path('../inputs/day_05_test.txt').read_text()
    real_data = Path('../inputs/day_05.txt').read_text()

    in_seeds, in_translations = parse_input(test_data)
    print(part_1(in_seeds, in_translations))
    print(part_2(in_seeds, in_translations))

    in_seeds, in_translations = parse_input(real_data)
    print(part_1(in_seeds, in_translations))
    print(part_2(in_seeds, in_translations))
