Advent of Code 2023
===================

Advent of code 2022 done in... I don't know. Python by default I guess.

Table of contents
-----------------

- [Day 1 - Trebuchet?!][d01]


Day 1 - Trebuchet?!
------------------------

[Solution][d01-py] - [Back to top][top]

We have a list of strings with digits mixed into them. For each line we want a
number made by the leftmost and rightmost digit on the line, which we'll need
to sum to solve the first part. Regexes to the rescue!

Finding the first digit inside a string is a simple matter of
`re.search('\d', s).group()` and for the last one we can simply reverse the
string and apply the same regex. To solve part one we just need to iterate
over every line of the input.

```python
def part_1(data):
    sum = 0
    for line in data.rstrip().split('\n'):
        first = re.search('\d', line).group()
        last = re.search('\d', line[::-1]).group()
        sum += int(first) * 10 + int(last)
    return sum
``` 

For part two we add a complication: the digits on each line can be spelled out.
I think we can adapt the solution for part one...

We start defining a dictionary of digits

```python
digits = {
    'one':   1, 'two':   2, 'three': 3,
    'four':  4, 'five':  5, 'six':   6,
    'seven': 7, 'eight': 8, 'nine':  9
}
```

with the keys to the dictionary we can build a new regex

```python
regex = '|'.join(digits.keys())
```

and adding a `|\d` at the end we can match for digits too. Matching on the reversed
string wont work... unless we reverse the regex too ;-) (and the matced string too!)

```python
xereg = regex[::-1]
```

and like before we can find the first and last digits with

```python
first = re.search(regex + r'|\d', line).group()
last = re.search(xereg + r'|\d', line[::-1]).group()[::-1]
```

with a simple helper we can convert what we found numbers and solve part two

```python
def to_int(s):
    if s.isdigit():
        return int(s)
    return digits[s]

def part_2(data):
    sum = 0
    regex = '|'.join(digits.keys()) 
    xereg = regex[::-1]

    for line in data.rstrip().split('\n'):
        first = re.search(regex + r'|\d', line).group()
        last = re.search(xereg + r'|\d', line[::-1]).group()[::-1]
        sum += to_int(first) * 10 + to_int(last)
    return sum
```

---
[top]: #advent-of-code-2022

[d01]: #day-1---calorie-counting


[d01-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_01.py
