#!/usr/bin/env python3
from collections import namedtuple
from itertools import combinations, pairwise
from pathlib import Path


TEST_INPUT = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

Point = namedtuple("Point", ["x", "y"])


class Polygon:
    def __init__(self, corners):
        self.corners = corners
        self.corner_set = set(corners)
        self.edges = [(a, b) for a, b in pairwise(corners + [corners[0]])]

    def contains_point(self, p):
        if p in self.corner_set:
            return True

        inside = False
        for a, b in self.edges:
            if a.y == b.y:
                if p.y == a.y and min(a.x, b.x) <= p.x <= max(a.x, b.x):
                    # point lies on a horizontal hedge
                    return True
            elif a.x == b.x:
                if p.y == a.y and min(a.x, b.x) <= p.x <= max(a.x, b.x):
                    # point lies on a vertical edge
                    return True
                else:
                    if a.x > p.x and min(a.y, b.y) <= p.y < max(a.y, b.y):
                        # a ray cast to the right from `p` crosses this edge
                        inside = not inside
            else:
                raise AssertionError(f"Invalid egde: {a} -> {b}")

        return inside

    def intersects_rect(self, r1, r2):
        for a, b in self.edges:
            rx_min, rx_max = min(r1.x, r2.x), max(r1.x, r2.x)
            ry_min, ry_max = min(r1.y, r2.y), max(r1.y, r2.y)
            if a.x == b.x:
                y_min, y_max = min(a.y, b.y), max(a.y, b.y)
                if rx_min < a.x < rx_max:
                    if y_min < ry_max and y_max > ry_min:
                        return True
            elif a.y == b.y:
                x_min, x_max = min(a.x, b.x), max(a.x, b.x)
                if ry_min < a.y < ry_max:
                    if x_min < rx_max and x_max > rx_min:
                        return True
            else:
                raise AssertionError(f"Invalid egde: {a} -> {b}")

        return False


def parse_input(input):
    return [Point(*map(int, l.split(","))) for l in input.splitlines()]


def area(rect):
    """Calculate the area of the rectangle between the two given corners"""
    return (abs(rect[1].y - rect[0].y) + 1) * (abs(rect[1].x - rect[0].x) + 1)


def part_1(corners):
    return area(max(combinations(corners, 2), key=area))


def part_2(corners):
    poly = Polygon(corners)

    res = 0
    for c1, c2 in combinations(corners, 2):
        for p in [
            Point(c1.x, c1.y),
            Point(c1.x, c2.y),
            Point(c2.x, c1.y),
            Point(c2.x, c2.y),
        ]:
            if not poly.contains_point(p):
                continue

        if poly.intersects_rect(c1, c2):
            continue

        res = max(res, area((c1, c2)))

    return res


if __name__ == "__main__":
    test_data = parse_input(TEST_INPUT)
    data = parse_input(Path("../inputs/day_09.txt").read_text())
    print(part_1(test_data))
    print(part_1(data))
    print(part_2(test_data))
    print(part_2(data))
