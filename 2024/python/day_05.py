#!/usr/bin/env python3
from functools import cmp_to_key
from pathlib import Path


def parse_input(data):
    rules, updates = data.split('\n\n')
    rules = [rule.split('|') for rule in rules.splitlines()]
    rules = [(int(r1), int(r2)) for r1, r2 in rules]
    updates = [{ int(page): pos 
                for pos, page in enumerate(update.split(',')) } 
                for update in updates.splitlines()]

    return rules, updates

def is_good(rules, update):
    good = True
    for before, after in rules:
        if before in update and after in update and not update[before] < update[after]:
            good = False
    return good

def part_1(rules, updates):
    good_ones = filter(lambda u: is_good(rules, u), updates)
    s = 0
    for g in good_ones:
        pages = list(g.keys())
        s += pages[len(pages)//2]
    return s

def part_2(rules, updates):
    def compare_update(one, another):
        page1, pos1 = one
        page2, pos2 = another
        if (page1, page2) in rules:
            return pos2 - pos1
        elif (page2, page1) in rules:
            return pos1 - pos2
        return 0

    bad_ones = list(filter(lambda u: not is_good(rules, u), updates))
    fixed = [sorted(u.items(), key=cmp_to_key(compare_update)) for u in bad_ones]
    s = 0
    for f in fixed: 
        l = len(f)
        s += f[l//2][0]
    return s

if __name__ == '__main__':
    test_data = Path('../inputs/day_05_test.txt').read_text()
    data = Path('../inputs/day_05.txt').read_text()

    rules, updates = parse_input(test_data)
    print(part_1(rules, updates))
    print(part_2(rules, updates))

    rules, updates = parse_input(data)
    print(part_1(rules, updates))
    print(part_2(rules, updates))
