#!/usr/bin/env python3
from collections import defaultdict
from itertools import combinations
from math import dist, prod
from pathlib import Path


TEST_INPUT = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""


class DisjointSet:
    def __init__(self, size):
        self.roots = list(range(size))

    def find(self, x):
        if self.roots[x] == x:
            return self.roots[x]
        else:
            return self.find(self.roots[x])

    def union(self, x, y):
        r_x, r_y = self.find(x), self.find(y)
        if r_x != r_y:
            self.roots[r_y] = r_x
        return r_x != r_y

    def subsets(self):
        subsets = defaultdict(list)
        for i in self.roots:
            subsets[self.find(i)].append(i)
        return subsets


def parse_input(input):
    return [tuple(map(int, l.split(","))) for l in input.splitlines()]


def sorted_pairs(points):
    index = range(len(points))
    return sorted(
        combinations(index, 2), key=lambda p: dist(points[p[0]], points[p[1]])
    )


def part_1(points, rounds):
    ds = DisjointSet(len(points))

    pairs = sorted_pairs(points)
    for a, b in pairs[:rounds]:
        ds.union(a, b)

    circuits = ds.subsets()
    sizes = sorted([len(v) for v in circuits.values()], reverse=True)
    return prod(sizes[:3])


def part_2(points):
    ds = DisjointSet(len(points))

    circuits = len(points)
    pairs = sorted_pairs(points)
    for a, b in pairs:
        circuits -= 1 if ds.union(a, b) else 0
        if circuits == 1:
            return points[a][0] * points[b][0]
    return 0


if __name__ == "__main__":
    test_data = parse_input(TEST_INPUT)
    data = parse_input(Path("../inputs/day_08.txt").read_text())
    print(part_1(test_data, 10))
    print(part_1(data, 1000))
    print(part_2(test_data))
    print(part_2(data))
