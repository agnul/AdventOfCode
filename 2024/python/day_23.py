#!/usr/bin/env python3
from collections import defaultdict
from pathlib import Path

def parse_input(data):
    network = defaultdict(set)
    for line in data.splitlines():
        l, r = line.split('-')
        network[l].add(r)
        network[r].add(l)
    return network

def part_1(network):
    triples = set()
    for a in network:
        for b in network[a]:
            for c in network[a] & network[b]:
                triples.add(tuple(sorted([a, b, c])))
    return len([t for t in triples if any(c.startswith('t') for c in t)])

def bron_kerbosch(N, R, P, X):
    if not P or X:
        yield R
    while P:
        v = P.pop()
        yield from bron_kerbosch(N, R | {v} , P & N[v], X & N[v])
        X.add(v)

def part_2(network):
    return ','.join(sorted(max(bron_kerbosch(network, set(), set(network.keys()), set()), key=len)))

if __name__ == '__main__':
    test_input = Path('../inputs/day_23_test.txt').read_text()
    real_input = Path('../inputs/day_23.txt').read_text()

    test_net = parse_input(test_input)
    real_net = parse_input(real_input)
    print(part_1(test_net))
    print(part_1(real_net))
    print(part_2(test_net))
    print(part_2(real_net))
