Advent of Code 2024
===================

Advent of code 2024 done in... think of Python like my equivalent of [Chef
Jean-Pierre Emotional Support Butter][butter]. 

Table of contents
-----------------
- [Day 1: Historian Hysteria][d01]
- [Day 2: Red-Nosed Reports][d02]


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

---
[top]: #advent-of-code-2023

[d01]: #day-1---historian-hysteria
[d02]: #day-2---red-nosed-reports

[d01-py]: https://github.com/agnul/AdventOfCode/blob/main/2024/python/day_01.py
[d02-py]: https://github.com/agnul/AdventOfCode/blob/main/2024/python/day_02.py
[d03-py]: https://github.com/agnul/AdventOfCode/blob/main/2024/python/day_03.py

[butter]: https://www.youtube.com/watch?v=HvT071_HVqA&t=312s
