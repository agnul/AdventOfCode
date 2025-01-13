#!/usr/bin/env python3
from itertools import batched
from pathlib import Path

def parse_input(data):
    inputs, circuit = data.split('\n\n')
    inputs = { signal: value == '1' for signal, value in
               batched(inputs.replace(': ', ' ').split(), 2) }
    circuit = { dst: (l, op, r) for l, op, r, dst in
                batched(circuit.replace(' -> ', ' ').split(), 4) }
    return inputs, circuit

def ev(inputs, gates, g):
    if g in inputs:
        return inputs[g]
    i0, op, i1 = gates[g]
    if op == 'AND':
        return ev(inputs, gates, i0) and ev(inputs, gates, i1)
    if op == 'OR':
        return ev(inputs, gates, i0) or ev(inputs, gates, i1)
    if op == 'XOR':
        a, b = ev(inputs, gates, i0), ev(inputs, gates, i1)
        return (a or b) and not a == b
    raise AssertionError(f'Invalid gate {op}')

def debug(circuit):
    adders = [None] * 45
    errs = []
    for g in circuit:
        i0, op, i1 = circuit[g]
        if op == 'XOR':
            if i0.startswith('x') or i0.startswith('y'):
                i = int(i0[1:])
                if not adders[i]: adders[i] = {}
                adders[i]['inputs'] = (i0, i1)
            elif g.startswith('z'):
                i = int(g[1:])
                if not adders[i]: adders[i] = {}
                adders[i]['output'] = (i0, i1)
            else:
                print(f'{g} should not be the result of {i0} {op} {i1}')
                errs.append(g)
        elif op == 'AND':
            if i0.startswith('x') or i0.startswith('y'):
                i = int(i0[1:])
                if not adders[i]: adders[i] = {}
                adders[i]['carry'] = (i0, i1)
        elif op == 'OR':
            pass
        else:
            raise AssertionError(f'Invalid gate {op}.')
    return adders


def part_1(inputs, gates):
    z_bits = { b: ev(inputs, gates, b)
               for b in filter(lambda s: s.startswith('z'), gates.keys()) }
    z = 0
    for k in sorted(z_bits.keys(), reverse=True):
        z = z * 2 + (1 if z_bits[k] else 0)
    return z

if __name__ == '__main__':
    test_inputs, test_circuit = parse_input(
        Path('../inputs/day_24_test.txt').read_text())
    print(part_1(test_inputs, test_circuit))

    inputs, circuit = parse_input(
        Path('../inputs/day_24.txt').read_text())
    print(part_1(inputs, circuit))

    print(debug(circuit))
