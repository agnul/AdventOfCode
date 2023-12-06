Advent of Code 2023
===================

Advent of code 2022 done in... I don't know. Python by default I guess.

Table of contents
-----------------

- [Day 1 - Trebuchet?!][d01]
- [Day 2 - Cube Conundrum][d02]
- [Day 3 - Gear Ratios][d03]
- [Day 4 - Scratchcards][d04]
- [Day 5 - If You Give A Seed A Fertilizer][d05]
- [Day 6 - Wait For It][d06]


Day 1 - Trebuchet?!
-------------------

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


Day 2 - Cube Conundrum
----------------------

[Solution][d02-py] - [Back to top][top]

We're given a list of games, each consisting of multiple drafts of colored cubes.
In part one we want to know which games are possible with a limited number of
cubes for each color. We start parsing the input into a dictionary of lists of
cube drafts:

```python
def parse_draft(cube_pairs):
    draft = defaultdict(int)
    for cnt_color in cube_pairs.split(','):
        cnt, color = cnt_color.split()
        draft[color] = int(cnt)

    return draft

def parse_input(data):
    games = {}
    for line in data.rstrip().split('\n'):
        (game_id, drafts) = line.split(':')
        games[int(game_id[5:])] = [parse_draft(d) for d in drafts.split(';')]

    return games
```

With 12 red, 13 green and 14 blue cubes available we are asked to find which of
the listed games is possible. Each game is possible if all of its cube drafts are
possible, and each draft is possible if it contains no more of the number of
available cubes for each color. We can then solve part one:

```python
def draft_is_possible(draft):
    return draft['red'] <= 12 and draft['green'] <= 13 and draft['blue'] <= 14

def part_1(games):
    game_is_possible = lambda gid: all(draft_is_possible(d) for d in games[gid])

    return sum(filter(game_is_possible, games.keys()))
```

In part two we are asked to find how many cubes of each color are needed for all
the games to be possible. The solution to part two is the sum of the products of
the minimun number of cubes for each color for each game.

```python
def power(game):
    min_r = min_g = min_b = 0
    for draft in game:
        min_r = max(min_r, draft['red'])
        min_g = max(min_g, draft['green'])
        min_b = max(min_b, draft['blue'])
    return min_r * min_g * min_b

def part_2(games):
    return sum(power(game) for game in games.values())
```

Day 3 - Gear Ratios
-------------------

[Solution][d03-py] - [Back to top][top]

We're given a grid of _symbols_ and numbers, where a symbol is anything that's
not a digit or a `.` character. For part one we want the sum of all the numbers
in the grid that are touching a symbol either above, below, left, right or
diagonally.

We start looking for the numbers, and since I suspect symbols will be useful
in part two we'll build a list of tuples mad up by a symbol and a list of the
numbers connected to it.

```python
def parse(grid):
    parts = []
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if not (char.isdigit() or char == '.'):
                parts.append((char, find_part_numbers(grid, i, j)))
    return parts
```

To find the numbers connected to the symbol at position `(r, c)` we can search
rows `r-1`, `r` and `r+1` for numbers and check that the leftmost or rightmost
digits are next to column `c`.

```python
def find_part_numbers(grid, row, col):
    res = []
    rows = len(grid)
    for i in [max(0, row - 1), row, min(rows, row + 1)]:
        for left, right in map(re.Match.span, re.finditer(r'\d+', grid[i])):
            if left - 1 <= col <= right:
                res.append(int(grid[i][left:right]))
    return res
```

With all that in place part one is pretty simple

```python
def part_1(data):
    return sum((sum(ns) for _, ns in data))
```

For part two we want only the _gear_ symbols, represented by the `*`
character, and of those we only want the ones connected to exactly two
numbers. Once we have them we want the sum of the products.

```python
def part_2(data):
    gears = filter(lambda d: d[0] == '*' and len(d[1]) == 2, data)
    return sum(a * b for _, [a, b] in gears)
```


Day 4 - Scratchcards
--------------------

[Solution][d04-py] - [Back to top][top]

We're given a list of "scratchcards", each made of a card number, some numbers on
the card, and some other numbers that we're told are the winning numbers. For each
card we can compute a score based on how many of the winning numbers (on the right
side of the `|`) sign appear on the card (the left side of the `|` sign). A single
number scores one point, each one after that doubles the score.

We can parse the input into a list of dicts, one for each card.

```python
def parse_input(data):
    cards = []
    for line in data.splitlines():
        card, numbers, winners = re.split(r'[:|]', line)
        cards.append({
            'card': int(card[5:]),
            'numbers': set(re.findall(r'\d+', numbers)),
            'winners': set(re.findall(r'\d+', winners))
        })
    return cards
```

and with that we can easily solve parte one: if we add the numbers on both sides
to two sets then the size of the set intersection of the two is the number `n` of
winning numbers on the card. The score is simply `2` to the power of `n - 1` and the
sum of the scores for each card is our solution

```python
def part_1(cards):
    sum = 0
    for c in cards:
        winning = c['numbers'].intersection(c['winners'])
        sum += 2 ** (len(winning) - 1) if winning else 0
    return sum
```

For part two we're told the game works a little differently: if on card `c`
we have `w` winning numbers then we get `1` new copy of cards `c+1`, `c+2`
... `c+w`. We must of course be careful: if we have multiple copies of card
`c` then we repeat the above as many times. We're asked to find with how many
cards we end up after all the winning numbers on all the cards have been
checked out.

```python
def part_2(cards):
    counts = [1] * len(cards)
    for i, c in enumerate(cards):
        cards_won = len(c['numbers'].intersection(c['winners']))
        for w in range(1, cards_won + 1):
            counts[i + w] += counts[i]
    return sum(counts)
```

[Day 5 - If You Give A Seed A Fertilizer]
-----------------------------------------

[Solution][d05-py] - [Back to top][top]

Still waiting for the bruteforce of part-2 ;-)


[Day 6 - Wait For It]
---------------------

[Solution][d06-py] - [Back to top][top]

We're racing micro-boats! Each race lasts a fixed amount of milliseconds (the
first line in the input). Each boat is charged by waiting a certain number
of milliseconds and then runs for the remaining time in the race at a speed
equal to the time spent charging. We want to know in how many ways we can beat
the race distance record, i.e. charge the boat long enough. We can do it the
obvious way, simulating each race: the distance run after charging for `j`
millis in a race lasting `time` millis is just `j * (time - j)`, and terating
over all times and distances we can solve part one:

```python
def solve(data):
    times, distances = data.splitlines()
    times = [int(n) for n in re.findall(r'\d+', times)]
    distances = [int(n) for n in re.findall(r'\d+', distances)]

    res = 1
    for time, distance in zip(times, distances):
        winning = partial(lambda d, r: r > d, distance)
        run = partial(lambda t, j: j * (t - j), time)

        races = [run(j) for j in range(time + 1)]
        winners = list(filter(winning, races))

        res *= len(winners)

    return res

def part_1(data):
    return solve(data)
```

For part two we're told that what we thought were multiple times and distances
are in fact a single race, obtained removing all spaces between the numbers. The
solution for part one still works... _if slowly_.

```python
def part_2(data):
    return solve(data.replace(' ', ''))
```

There is a smarter way involving math ;-)

The distance covered by running for $x$ millis in a race $t$ millis long is

$$d = x(t - x)$$

We want all the values for $x$ for which

$$x(t - x) \geq d$$

or put another way

$$-x^2 + tx - d \geq 0$$

Using the formula from school we find

$$x_{min}=\frac{-t + \sqrt{t^2 -4d}}{-2}$$

$$x_{max}=\frac{-t - \sqrt{t^2 -4d}}{-2}$$

and the race is won for values

$$x_{min} \leq x \leq x_{max}$$

Translating all that in code (and adjusting for integers) we get

```python
def solve_fast(data):
    times, distances = data.splitlines()
    times = [int(n) for n in re.findall(r'\d+', times)]
    distances = [int(n) for n in re.findall(r'\d+', distances)]

    res = 1
    for time, distance in zip(times, distances):

        delta = sqrt(time**2 - 4*distance)
        x_min, x_max = (time - delta) / 2, (time + delta) / 2
        res *= (ceil(x_max) - floor(x_min) - 1)

    return res
```

---
[top]: #advent-of-code-2023

[d01]: #day-1---trebuchet
[d02]: #day-2---cube-conundrum
[d03]: #day-3---gear-ratios
[d04]: #day-4---scratchcards
[d05]: #day-5---if-you-give-a-seed-a-fertilizer
[d06]: #day-6---wait-for-it

[d01-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_01.py
[d02-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_02.py
[d03-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_03.py
[d04-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_04.py
[d05-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_05.py
[d06-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_06.py
