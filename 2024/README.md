Advent of Code 2024
===================

Advent of code 2024 done in... think of Python like my equivalent of [Chef
Jean-Pierre Emotional Support Butter][butter].

Table of contents
-----------------
- [Day 1: Historian Hysteria][d01]
- [Day 2: Red-Nosed Reports][d02]
- [Day 3: Mull It Over][d03]
- Day 4: Ceres Search - Uhg, grids. Don't want to.
- [Day 5: Print Queue][d05]
- Day 6: Guard Gallivant - Grids, see above.
- [Day 7: Bridge Repair][d07]
- Day 8: Resonant Collinearity - Looks like a grid...
- [Day 9: Disk Fragmenter][d09]
- Day 10: Hoof It - Another grid, eew.
- [Day 11: Plutonian Pebbles][d11]
- Day 12: Garden Groups - You would think I don't like grids...
- [Day 13: Day 13: Claw Contraption][d13]
- Day 14: Restroom Redoubt
- Day 15: Warehouse Woes
- Day 16: Reindeer Maze
- Day 17: Chronospatial Computer
- Day 18: RAM Run
- Day 19: Linen Layout
- Day 20: Race Condition
- Day 21: Keypad Conundrum
- [Day 22: Monkey Market][d22]
- [Day 23: LAN Party][d23]


Day 1 - Historian Hysteria
--------------------------

[Solution][d01-py] - [Back to top][top]

Short and simple: two columns of numbers, pair them smallest to smallest,
repeat for all numbers, sum the difference between resulting pairs.

In part two count how many times each number appears in the right column
and the go over each number in the left column and multiply it by the
number of times it occurs on the right, then sum all the results.

```python
def parse_input(data):
    numbers = [int(n) for n in data.split()]
    left = numbers[0::2]
    right = numbers[1::2]
    return left, right

def part_1(left, right):
    left, right = sorted(left), sorted(right)
    return sum(abs(r - l) for l, r in zip(left, right))

def part_2(left, right):
    counts = Counter(right)
    return sum (l * counts[l] for l in left)
```

Day 2 - Red-Nosed Reports
-------------------------

[Solution][d02-py] - [Back to top][top]

We've got some lists of numbers, for each list we want to make sure that
items are always increasing or decreasing, and the difference between each
pair of consecutive ones is at least one and at most three. Count the
'good' sequences.

In part two we must to the same, with the twist that a sequence is also
'good' if removing at most one of the items the above holds.

```python
def parse_input(data):
    return [[int(n) for n in l.split()] for l in data.splitlines()]

def increasing(report):
    return [(a < b and b - a <= 3) for a, b in zip(report, report[1:])]

def decreasing(report):
    return [(a > b and a - b <= 3) for a, b in zip(report, report[1:])]

def is_safe(report):
    return all(increasing(report)) or all(decreasing(report))

def can_apply_dampener(report):
    return any([is_safe(report[0:i] + report[i+1:]) for i in range(len(report))])

def part_1(reports):
    return len([r for r in reports if is_safe(r)])

def part_2(reports):
    return len([r for r in reports if is_safe(r) or can_apply_dampener(r)])
```

Day 3 - Mull It Over
--------------------

[Solution][d03-py] - [Back to top][top]

We have a string that contains what looks like code: we want to find all
the multiplication instructions and execute them, summing the resuts. Looks
like a job for regexes!

```python
def part_1(mem):
    res = 0
    for m in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)", mem):
        res += int(m.group(1)) * int(m.group(2))
    return res
```

In part two we're looking for multiplication and two more instructions, `do`
and `don't`. We start multiplying, stop as soon as we find a `don't` and
resume when we find a `do`. A little tweak to the above is all we need.

```python
def part_2(mem):
    mul, res = True, 0
    for m in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))", mem):
        if m.group(3) == 'do()':
            mul = True
        elif m.group(4) == "don't()":
            mul = False
        elif mul:
            l, r = int(m.group(1)), int(m.group(2))
            res += l * r
    return res
```

Day 5 - Print Queue
-------------------

[Solution][d05-py] - [Back to top][top]

We got some pairs of numbers (let's call them rules) and some lists of
numbers (let's call them updates). We want to make sure that if both numbers
in one rule appear in the update then they must be in the order specified by
the rule. Part one wants us to find which updates are OK and then to sum the
middle number in each such update

```python
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
```

In part two we want to fix the updates we rejected in part one and again sum the
middle numbers. We just filter the bad ones, define a compare function that will
allow us to sort updates and we're done

```python
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
```

Coul'd have beed definitely smarter in chosing my data structures, as usual check
[Hyperneutrino's solution][hn-day5]

Day 7 - Bridge Repair
---------------------

[Solution][d07-py] - [Back to top][top]

We've got the usual lists of numbers: for each one we want to know if we can get
the number on the left adding the missing addiction and multiplication signs on
the right. Part two adds string concatenation to the possible operations:

```python
def parse_input(data):
    res = []
    for line in data.splitlines():
        goal, numbers = line.split(':')
        res.append([int(goal), [int(n) for n in numbers.split()]])
    return res

def cat(n1, n2):
    return int(str(n1) + str(n2))

def sat(goal, current, numbers, pt2=False):
    if len(numbers) == 1:
        if goal == current + numbers[0]: return True
        if goal == current * numbers[0]: return True
        return pt2 and goal == cat(current, numbers[0])

    if sat(goal, current + numbers[0], numbers[1:], pt2): return True
    if sat(goal, current * numbers[0], numbers[1:], pt2): return True
    return pt2 and sat(goal, cat(current, numbers[0]), numbers[1:], pt2)

def part_1(data):
    return sum(goal for goal, numbers in data if sat(goal, numbers[0], numbers[1:]))

def part_2(data):
    return sum(goal for goal, numbers in data if sat(goal, numbers[0], numbers[1:], True))
```

The recursive function could have taken one less argument, but it came out
like that and it works, so... `¯\_(ツ)_/¯`

Day 9 - Disk Fragmenter
-----------------------

[Solution][d09-py] - [Back to top][top]

We have a list of numbers that taken in pairs represent a map of
allocated/free space. We want to progressively move allocated blocks from the
right hand side to the free blocks on the left side and then calculare some sort
of checksum

```python
def parse_input(data):
    disk = []
    for id, pair in enumerate(batched(data, 2)):
        sz = pair[0]
        free = pair[1] if len(pair) == 2 else 0
        disk += [id] * int(sz) + ['.'] * int(free)
    return disk

def part_1(data):
    i, j, disk = 0, len(data) - 1, []
    while i <= j:
        if data[i] != '.':
            disk.append(data[i])
            i += 1
        elif data[j] != '.':
            disk.append(data[j])
            i += 1
            j -= 1
        else:
            j -= 1
    total = len([d for d in data if d != '.'])
    return sum(i * int(n) for i, n in enumerate(disk))
```

... and that will not work for part 2.

Day 11 - Plutonian Pebbles
--------------------------

[Solution][d11-py] - [Back to top][top]

We've got some numbers that change over time: `0`s become `1`s, numbers
with an even number of digits split into their left and right halves,
everything else gets multiplied by `2024`. We want to know how many numbers
are there after some fixed number of iterations of the above. Since the
numbers are never combined but each one 'evolves' separately we can do
them one at a time and we're very likely to be encounter the same numbers
over and over, so caching them seems like a good idea:

```python
def parse_input(data):
    return [int(_) for _ in data.split()]

def blink(cache, stone, times):
    if (stone, times) in cache:
        return cache[(stone, times)]

    if times == 0:
        return 1

    s_stone = str(stone)
    s_len = len(s_stone)
    if stone == 0:
        cache[(stone, times)] = blink(cache, 1, times - 1)
    elif s_len % 2 == 0:
        left = int(s_stone[:s_len//2])
        right = int(s_stone[s_len//2:])
        cache[(stone, times)] = blink(cache, left, times - 1) + blink(cache, right, times - 1)
    else:
        cache[(stone, times)] = blink(cache, stone * 2024, times - 1)

    return cache[(stone, times)]

def part_1(data):
    cache = {}
    return sum(blink(cache, stone, 25) for stone in data)

def part_2(data):
    cache = {}
    return sum(blink(cache, stone, 75) for stone in data)
```

Don't reinvent the wheel. Use `functools.cache` ;-) Also doing `int` to `str` and back may
not be the most efficient, but it looks like it's fast enough.

Day 13 - Claw Contraption
-------------------------

[Solution][d03-py] - [Back to top][top]

That looks suspiciously like a system of linear equations. Brush up on
[Cramer's rule][cramer], parse the input and it's done. Note that we only
want the integer solutions.

```python
def parse_input(data):
    eqs = []
    for eq in data.split('\n\n'):
        lines = eq.splitlines()
        a1, a2 = [int(_) for _ in re.findall(r'\d+', lines[0])]
        b1, b2 = [int(_) for _ in re.findall(r'\d+', lines[1])]
        c1, c2 = [int(_) for _ in re.findall(r'\d+', lines[2])]
        eqs.append([[a1, b1], [a2, b2], [c1, c2]])
    return eqs

def solve(eq):
    a1, b1 = eq[0]
    a2, b2 = eq[1]
    c1, c2 = eq[2]

    det = a1 * b2 - b1 * a2
    if det == 0:
        return None

    a, ra = divmod(c1 * b2 - b1 * c2, det)
    b, rb = divmod(a1 * c2 - c1 * a2, det)

    return (a, b) if ra == 0 and rb == 0 else None


def part_1(eqs):
    return sum(a * 3 + b for a, b in [solve(eq) for eq in eqs if solve(eq)])
```

In part two we just need to add a huge number to the 'claw' positions and solve
the same equation. Huge numbers are not a problem for python so...

```python
def part_2(eqs):
    for eq in eqs:
        eq[2][0] += 10000000000000
        eq[2][1] += 10000000000000
    return part_1(eqs)
```


Day 22: Monkey Business
-----------------------

[Solution][d22-py] - [Back to top][top]

We have a bunch of numbers that we need to _evolve_ two thousand times. Part one
wants us to sum the remainders of dividing each eveolved number by ten. (Bitwise
operations because they're fun, not that it will save any time in python)

```python
def evolve(initial, rounds=1):
    res = initial
    for _ in range(rounds):
        res = ((res <<  6) ^ res) & 0xffffff
        res = ((res >>  5) ^ res) & 0xffffff
        res = ((res << 11) ^ res) & 0xffffff
    return res


def part_1(secrets):
    return sum(evolve(s, 2000) for s in secrets)
```

In part two we're still evolving the above numbers, but we want to keep track
of how they change after each round, saving the last four differences between
a value and the previous one. Each sequence of four differences could appear
multiple times in the evolution of a single initial number and could (or could
not) appear independently in the evolution of each initial number. For each
one of those we care only for the initial occurrence of a given four-difference
sequence, at which time we save the value (modulo ten) of the fifth eveolved
number.

```python
def part_2(secrets):
    sales = defaultdict(int)
    for s in secrets:
        seen = set()
        window = deque([s], maxlen=5)
        for _ in range(1999):
            window.append(evolve(window[-1]))
            if len(window) < 5:
                continue
            diffs = tuple(window[i] % 10 - window[i-1] % 10 for i in range(1, 5))
            if diffs in seen:
                continue
            seen.add(diffs)
            sales[diffs] += window[-1] % 10
    return max(sales.values())
```


Day 23: LAN Party
-----------------

[Solution][d23-py] - [Back to top][top]

We've got a series of string pairs representing (directionless) connections
between computers and we want to determine the groups of those computers that
are completely interconnected. (Note for me: if `a` is connected to `b` and `c`
those are not completely interconnected since there's no connection between
`b` and `c` ;-))

Part one wants us to count the groups of three completely connected computers
in which at least one computer name starts with `t`. Suppose we represent our
network as a map from a computer to the set of computers to which it has a
direct connection

```python
def parse_input(data):
    network = defaultdict(set)
    for line in data.splitlines():
        l, r = line.split('-')
        network[l].add(r)
        network[r].add(l)
    return network
```

then we can for each computer in the network check if any of the computers
the initial one is connected to has some connections in common. Note that
`a-b-c` is the same ad `c-a-b` so we sort the computer names to keep the
triplets unique

```python
def part_1(network):
    triples = set()
    for a in network:
        for b in network[a]:
            for c in network[a] & network[b]:
                triples.add(tuple(sorted([a, b, c])))
    return len([t for t in triples if any(c.startswith('t') for c in t)])
```

Part two wants the computer names in the biggest set of interconnected
computers... and that sounds as a [max clique problem][clique] on a
graph for which we can blatantly copy the [algorith from wikipedia][bk-algo],
again taking advantage of python's `set`s. After iteratively findind all the
possible cliques we just take the maximum one sorting by length and concatenate
the correspoing computer names sorted alphabetically as requested.

```python
def bron_kerbosch(N, R, P, X):
    if not P or X:
        yield R
    while P:
        v = P.pop()
        yield from bron_kerbosch(N, R | {v} , P & N[v], X & N[v])
        X.add(v)

def part_2(network):
    return ','.join(sorted(max(bron_kerbosch(network, set(), set(network.keys()), set()), key=len)))
```

---
[top]: #advent-of-code-2024

[d01]: #day-1---historian-hysteria
[d02]: #day-2---red-nosed-reports
[d03]: #day-3---mull-it-over
[d05]: #day-5---print-queue
[d07]: #day-7---bridge-repair
[d09]: #day-9---disk-fragmenter
[d11]: #day-11---plutonian-pebbles
[d13]: #day-13---claw-contraption
[d22]: #day-22---monkey-market
[d23]: #day-23---lan-party

[d01-py]: https://github.com/agnul/AdventOfCode/blob/main/2024/python/day_01.py
[d02-py]: https://github.com/agnul/AdventOfCode/blob/main/2024/python/day_02.py
[d03-py]: https://github.com/agnul/AdventOfCode/blob/main/2024/python/day_03.py
[d05-py]: https://github.com/agnul/AdventOfCode/blob/main/2024/python/day_05.py
[d07-py]: https://github.com/agnul/AdventOfCode/blob/main/2024/python/day_07.py
[d09-py]: https://github.com/agnul/AdventOfCode/blob/main/2024/python/day_09.py
[d11-py]: https://github.com/agnul/AdventOfCode/blob/main/2024/python/day_11.py
[d13-py]: https://github.com/agnul/AdventOfCode/blob/main/2024/python/day_13.py
[d22-py]: https://github.com/agnul/AdventOfCode/blob/main/2024/python/day_22.py
[d23-py]: https://github.com/agnul/AdventOfCode/blob/main/2024/python/day_23.py

[butter]: https://www.youtube.com/watch?v=HvT071_HVqA&t=312s
[cramer]: https://en.wikipedia.org/wiki/Cramer%27s_rule
[hn-day5]: https://www.youtube.com/watch?v=BHFnoc4bw3U
[clique]: https://en.wikipedia.org/wiki/Clique_problem
[bk-algo]: https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm

0432 491369
