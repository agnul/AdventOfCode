#!/usr/bin/env python3

TEST_INPUT = """..X...
.SAMX.
.A..A.
XMAS.S
.X....
"""

TEST_INPUT_2="""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

def parse_input(data):
    return ''.join(data.splitlines())

def p1(blob):
    cnt = 0
    for R in range(0, len(blob), 10):
        for C in range(L, )
        pass
    return cnt

def part_1(lines):
    cnt = 0
    for l in lines:
        for i in range(len(l) - 4):
            if 'XMAS' in l[i:] or 'SAMX' in l[i:]:
                cnt += 1
    cols = [''.join(c) for c in zip(*lines)]
    for c in cols:
        for i in range(len(c) - 4):
            if 'XMAS' in l[i:] or 'SAMX' in l[i:]:
                cnt += 1
    return cnt

if __name__ == '__main__':
    lines = parse_input(TEST_INPUT_2)
    print(lines)
    print(p1(lines))




