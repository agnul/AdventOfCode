#!/urs/bin/env python3
from pathlib import Path

TEST_DATA = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

def parse_input(data):
    parsed = []
    for line in data.splitlines():
        springs, groups = line.split()
        groups = tuple(map(int, groups.split(',')))
        parsed.append((springs, groups))
    return parsed


def none_is_broken(springs):
    return '#' not in springs


def none_is_good(springs):
    return '.' not in springs


def configurations(springs, groups, cache={}):
    if springs == '':
        return 1 if groups == () else 0

    if groups == ():
        return 1 if none_is_broken(springs) else 0

    key = (springs, groups)
    if key in cache:
        return cache[key]

    res = 0
    s, ss = springs[0], springs[1:]
    g, gs = groups[0], groups[1:]

    # good spring or guess good
    if s in '.?':
        res += configurations(ss, groups, cache)

    # broken spring or guess broken
    if s in '#?' and (len(springs) == g and none_is_good(springs[:g]) or
                      len(springs) > g and none_is_good(springs[:g]) and springs[g] != '#'):
        res += configurations(springs[g+1:], gs, cache)

    cache[key] = res
    return res


def part_1(data):
    return sum(configurations(springs, groups, {}) for springs, groups in data)


def part_2(data):
    return sum(configurations("?".join([springs] * 5), groups * 5, {}) for springs, groups in data)


if __name__ == '__main__':
    test_records = parse_input(TEST_DATA)
    print(part_1(test_records))
    print(part_2(test_records))

    records = parse_input(Path('../inputs/day_12.txt').read_text())
    print(part_1(records))
    print(part_2(records))
