Advent of Code 2023
===================

Advent of code 2022 done in... I don't know. Python by default I guess.

Table of contents
-----------------

- [Day 1 - Trebuchet?!][d01]
- [Day 2 - Cube Conundrum][d02]
- [Day 3 - Gear Ratios][d03]
- [Day 4 - Scratchcards][d04]
- [Day 5 - If You Give A Seed A Fertilizer][d05]<sup>†</sup>
- [Day 6 - Wait For It][d06]
- [Day 7 - Camel Cards][d07]
- [Day 8 - Haunted Wasteland][d08]
- [Day 9 - Mirage Maintenance][d09]
- [Day 10 - Pipe Maze][d10]
- [Day 11 - Cosmic Expansion][d11]
- [Day 12 - Hot Springs][d12]
- [Day 13 - Point of Incidence][d13]
- [Day 14 - Parabolic Reflector Dish][d14]
- [Day 15 - Lens Library][d15]
- [Day 16 - The Floor Will Be Lava][d16]
- [Notes][notes]


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

Today we're moving some _seed_ positions through a series of translations
to a final _soil_ position. Our input is made of a list of initial positions
and a series of translations of the form `(dst, src, count)` meaning that
each numbers between `src` and `src + count` has to be translated to a new
position between `dst` and `dst + count`. We can start by parsing the input:

```python
def parse_block(block):
    parse_line = lambda l: map(int, re.findall(r'\d+', l))

    return [tuple(t) for t in map(parse_line, block.splitlines()[1:])]

def parse_input(lines):
    blocks = lines.split('\n\n')
    seeds = list(map(int, re.findall(r'\d+', blocks[0])))

    return seeds, [parse_block(b) for b in blocks[1:]]
```

which will return the initial _seed_ positions and a list of lists of
tuples representing the transformations.

Part 1 is simple enough: go through each seed and try to apply each
transformation in sequence. Our answer is the minimum of the new
positions once all possible translations are applied.

```python
def translate(seed, trans):
    for dst, src, size in trans:
        if src <= seed < src + size:
            return dst + seed - src
    return seed

def part_1(seeds, translations):
    soils = []
    for seed in seeds:
        for trans in translations:
            seed = translate(seed, trans)
        soils.append(seed)
    return min(soils)
```

In part 2 we're told that the _seeds_ on the first line of the input are no
longer individual seeds but taken in pairs they make up a list of seed
intervals of the form `(start, count)` and we're to apply the same
translations as before to these. One could reuse the code for part 1 and
brute-force the solution enumerating all of the seeds in the intervals but
a quick check shows that could take some time... a smarter solution is
required. Taking a look at the data shows that the seed_intervals and the
translation ranges don't overlap perfectly so we can't translate just the
seed_interval extremes, but we should apply each translation only to the
overlapping parts and leave the non-overlapping parts for processing by
later translations. We face four possible cases:

Non overlapping intervals:

```text

   S---seeds---T        A---trans---B
```

Overlapping intervals:

```text
    A---trans---B               A---trans---B
          S---seeds---T     S---seeds---T
```

Fully contained intervals:

```text
            S---seeds---T
         A-------trans-------B
```

We can apply the translation to the overlapping parts, leaving like this:

```python
def translate_pt2(seed_intervals, translations):
    done = []
    while seed_intervals:
        start, count = seed_intervals.pop()
        for dst, src, size in translations:
            left = max(start, src)
            right = min(start + count, src + size)
            if left < right:
                done.append((left + (dst - src), right - left))
                if left > start:
                    seed_intervals.append((start, left - start))
                if start + count > right:
                    seed_intervals.append((right, start + count - right))
                break
        else:
            done.append((start, count))
    return done
```

where `left` and `right` delimit the overlapping part, `start` and `count`
represent a seed interval and the `(dst, src, size)` tuples represent a
translation. The function above will return a modified version of the
seed intervals containing the parts that have successfully been translated
and the parts that did not overlap with any translation. For part 2 we then
just need to create the seed intervals and apply the above to every block
of translations in the input

```python
def part_2(seeds, translation_blocks):
    seed_intervals = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]

    for block in translation_blocks:
        seed_intervals = translate_pt2(seed_intervals, block)
    return min(seed_intervals)[0]
```

The same could be applied for part 1 if we consider each seed an interval
of length 1:

```python
def part_1b(seeds, translations):
    seed_intervals = [(s, s+1) for s in seeds]
    for trans in translations:
        seed_intervals = translate_pt2(seed_intervals, trans)
    return min(seed_intervals)[0]
```


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


Day 7 - Camel Cards
-------------------

[Solution][d07-py] - [Back to top][top]


In day 7 we're playing a simplified game of poker. We're given a list of hands
and bids, and we're asked to sort them by their _rank_ and then sum the product
of each hand's position by the associated bid. Sorting should be easy: the one
with the most cards of the same type wins (five of a kind, four of a kind, full
house... you get the idea), and hands of the same type are ranked by the
highest card from left to right. Cards are (low to high), 2, 3, 4 ... 9, T,
J, Q, K and A. Parsing the input is just a matter of calling `splitlines()`.
As for sorting we could turn each hand in a suitable string and sort the
results lexicografically. To count the number of equal cards Python's
`Counter` is useful. Doing something like

```python
''.join(map(str, sorted(Counter(hand).values(), reverse=True)))
```

will result in `5` for five-of-a-kind hands, `41` for four-of-a-kind,
`32` for full-house and so on and sorting those lexicographically
has the weakest hands first and the strongest hands last

```text
11111 - highest card
2111  - one par
221   - two pairs
311   - three of a kind
32    - full house
41    - four of a kind
5     - five of a kind
```

To sort hands of the same strenght we can't use the cards value because
we want `T` before `J`, `Q` before `K` and `A` last, so using the card
values won't work. But we could just translate them into different letters
like, for example

```text
23......A
vv......v
AB......M
```

and the resulting strings would be ordered the way we need. Putting it
all together...

```python
def hand_type(hand_and_bid):
    return ''.join(map(str, sorted(Counter(hand_and_bid[:5]).values(), reverse=True)))

def hand_strength(hand, hand_type_fn, face_values):
    return hand_type_fn(hand) + ''.join(face_values[c] for c in hand)

def solve(data, card_strength, face_values):
    key_fn = lambda line: hand_strength(line[:5], card_strength, face_values)
    winnings = 0
    for i, line in enumerate(sorted(data, key=key_fn), start=1):
        winnings += i * int(line[6:])
    return winnings

def part_1(data):
    face_values = dict(zip('23456789TJQKA', 'ABCDEFGHIJKLM'))
    return solve(data, hand_type, face_values)

```

Maybe putting the two sorting keys into a tuple instead of sticking thenm
together in a single string would have been nicer, but this way works too.

Part 2 adds Jokers. `J` cards can now take the value of each other card
when ranking hand types, but are lower than `2` when considering face value.
The same trick as before works, once we figure out what to do with jokers.
The winning strategy is to turn all of the jokers into the most common one:
if you have a pair and two jokers you could turn your hand into two pairs,
three of a kind, a full-house... but the obvious choice is the four of a kind
hand.

```python
def hand_type_with_jokers(hand_and_bid):
    hand = hand_and_bid[:5].replace('J', '')
    jokers = 5 - len(hand)
    counts = sorted(Counter(hand).values(), reverse=True)
    if jokers < 5:
        counts[0] += jokers
    else:
        counts = [5]
    return ''.join(map(str, counts))
```

With that, and adjusting for the `J` card to sort before `2` part 2 is

```python
def part_2(data):
    face_values = dict(zip('J23456789TQKA', 'ABCDEFGHIJKLM'))
    return solve(data, hand_type_with_jokers, face_values)
```


[Day 8 - Haunted Wasteland]
---------------------------

[Solution][d08-py] - [Back to top][top]

In day 8 we're kina traversing a map: we have a list of directions to be
applied cyclically and a map saying if you are at `AAA` you can go left to
`BBB` or right to `CCC`. The first part asks how many steps it takes to
go from `AAA` to `ZZZ`.

There's not much parsing involved:

```python
def parse_input(data):
    directions, maps = data.split("\n\n")
    network  = {}
    for m in maps.splitlines():
        key, left, right = re.match(r'^(.*) = \((.*), (.*)\)$', m).groups()
        network[key] = (left, right)
    return directions, network
```

this will return a string of directions and a dictionary of `(left, right)`
tuples.

Part 1 is just a matter of repeatedly cycling over the directions (using
`itertools.cycle`) until we reach the `ZZZ` position:

```python
def walk(directions, maps):
    pos = 'AAA'
    for steps, dir in enumerate(cycle(directions)):
        if pos == 'ZZZ':
            break
        pos = maps[pos][0 if dir == 'L' else 1]
    return steps

def part_1(directions, maps):
    return walk(directions, maps)
```

Part 2 is obviously some million times more complex so the same brute force
approach won't work: we're to start simultaneously at each position ending
in `A` and stop when all the positions end in `Z`. It all could go terribly
wrong but what if each path was independent of the others and we could just
find those and try their [lcm][wiki-lcm]?

```python
def lcm(a, b):
    return a * b // math.gcd(a, b)

def walk_n(directions, maps):
    posns = [m for m in maps if m.endswith('A')]
    steps = [0] * len(posns)
    for dir in cycle(directions):
        if all(p.endswith('Z') for p in posns):
            break;
        for j, pos in enumerate(posns):
            if pos.endswith('Z'):
                continue
            posns[j] = maps[pos][0 if dir == 'L' else 1]
            steps[j] += 1
    return reduce(lcm, steps, 1)

def part_2(directions, maps):
    return walk_n(directions, maps)
```

That worked ;-)


Day 9 - Mirage Maintenance
--------------------------

[Solution][d09-py] - [Back to top][top]

In day 9 we're given lists of numbers. For each list we are told to reduce
the numbers calculating the pairwise differences until we get all zeroes.
Once there we're told we can deduce the next number for each of the initial
lists proceding backwards from the zeroes. Given the steps

```text
0   3   6   9  12  15
  3   3   3   3   3
    0   0   0   0
```

we're told if we were to add one more `0` to the right of the last line
then we'd have to add a number `n` to the line above so that `n - 3` equals
`0`, and so on for every line until the first one. In the example above we
would add `3` (because `3 - 3 = 0`) and 18 (because `18 - 15 = 3`).

For part 1 we must repeat the above and sum the numbers we would add to the
original list. If you look at it closely it's obvious that the number we're
looking for it's the sum of the last number on each line (in the above
example `0`, `3` and `15`). We start with a function to calculate the
pairwise differences

```python
def differences(line):
    nums = line
    deltas = [line]
    while any(nums):
        nums = [b - a for a, b in zip(nums, nums[1:])]
        deltas.append(nums)
    return deltas
```

then we can derive the last number on each line with

```python
def derive_last(line):
    return sum(d[-1] for d in differences(line)[::-1])
```

and finally solve part one like

```python
def part_1(lines):
    return sum(derive_last(line) for line in lines)
```

Part 2 asks to derive in much the same way the number we should add
at the beginning of each line. Given the example

```text
*5*  10  13  16  21  30  45
  *5*   3   3   5   9  15
   *-2*   0   2   4   6
      *2*   2   2   2
        *0*   0   0
```

we can see that we should start by adding `n` so that `2 - n` equals `0`,
then another `m` so that `0 - m` equals `-2` and so on. Trying the examples
it looks like each new number is the sum of the previous ones multiplied by
`-1` and added to the first existing number on the same line, so let's try
that:

```python
def derive_first(line):
    deltas = [d[0] for d in differences(line)]
    return reduce(lambda acc, d: -1 * acc + d, deltas[::-1])

def part_2(lines):
    return sum(derive_first(line) for line in lines)
```

That worked again ;-)


Day 10 - Pipe Maze
------------------

[Solution][d10-py] - [Back to top][top]

In day 10 we are playing with mazes. We're given a grid of characters that
contains a loop made of the character `S|-LJ7F` and we want to find the
farthest point from the loop's start `S`, which of course is at mid loop.
Each of the above symbols connects at most two grid positions, for example
`|` can connect the cell below and the cell above, `L` connects only to the
cell above and the cell to its right. The `S` symbol is the only one that
can connect any two of the four neighbourin cells. We can start by mapping
what connects to what and writing a function that finds the possible exits
from a given grid position (North is one grid row above, West is one grid
column to the left):

```python
PIPE_EXITS = {
    'S': [(-1, 0), (1, 0), (0, -1), (0, 1)],
    '|': [(-1, 0), (1, 0)],
    '-': [(0, -1), (0, 1)],
    'L': [(-1, 0), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    '7': [(1, 0), (0, -1)],
    'F': [(1, 0), (0, 1)]
}

def pipe_exits(grid, r, c):
    cur = grid[r][c]
    for dr, dc in PIPE_EXITS[cur]:
        xr = r + dr
        xc = c + dc
        if xr and 0 <= xc < len(grid[0]) and grid[xr][xc] in 'S|-LJ7F':
            yield xr, xc
```

Since we want the farthest point from the start of the loop we must first
find the loop: that can be done with a [Breadth First Search][wiki-bfs] or,
since each pipe only connects two grid cells, by following the pipes until
we're back to the start, making sure we exit each pipe from the opposite
end to the one we entered (that's the second-last cell in the loop or the
starting cell if the loop is shorter than two cells)

```python
def find_entry(grid):
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == 'S':
                return r, c
    return None

def find_loop(grid):
    start_r, start_c = find_entry(grid)

    loop = [(start_r, start_c)]

    closed_loop = False
    while not closed_loop:
        cur_r, cur_c = loop[-1]
        for r, c in pipe_exits(grid, cur_r, cur_c):
            if len(loop) < 2:
                loop.append((r, c))
                break
            elif loop[-2] != (r, c):
                loop.append((r, c))
                break
        closed_loop = (loop[-1] == (start_r, start_c))
    return loop
```

With that done part 1 is simply

```python
def part_1(grid):
    return len(find_loop(grid)) // 2
```

Part two wants us to find how many grid cells are fully enclosed by the maze,
that is are _inside_ the polygon formed by the pipes. I've got no idea how to
do that, but the internet has shown at least two ways ;-). [HyperNeutrino]
has done it by counting how many pipes a straight line originating at each
point on the grid would cross on the way to the grid border: for the points
inside the polygon that has to be an odd number... but then someone in the
comments pointed out that it could also be done applying something called
[Pick's Theorem][wiki-picks]. That one says that if we have a polygon on a
grid of integer coordinates its area is the numnber `i` of points inside the
polygon plus half the number `b` of the vertexes making up it's border minus
one

$$A = i \times \frac{b}{2} - 1$$

Now if we had another way to calculate the area... the same someone pointed
to the [Shoelace Formula][wiki-shoelace]: the area of a polygon with vertexes
at integer coordinates is a simple series of sums and multiplications.
Combining the two part two is simply

```python
def part_2(grid):
    loop = find_loop(grid)
    vertexes = len(loop)

    area = 0
    for (x1, y1), (x2, y2) in zip(loop, loop[1:]):
        area += x1 * y2 - y1 * x2

    area = abs(area) // 2
    return area + 1 - vertexes // 2
```

Day 11 - Cosmic Expansion
-------------------------

[Solution][d11-py] - [Back to top][top]

In day 11 we've got ourselves a universe made of galaxies (`#`) and empty
space `.`. Part one want's us to find the sum of the pairwise distances
between the galaxies, with the caveat that the universe is expanding: every
row and column in the grid that are made entirely of empty space doubles its
size. The distance between galaxies is the usual
[Manhattan's distance][wiki-taxicab]. There's no parsing involved, we'll
just `splitlines()` on the input. As for the rest of the code... we could
just simulate the universe and then calculate the galaxies' distances but I
suspect things could get out of hand with expansion. Why not just count the
rows and columns between pairs of galaxies taking into account expansion?
Count each row/column as `1` if a galaxy is found on the same row/colum, `2`
if it's empty.

```python
def solve(universe, expansion):
    empty_rows = [r for r, row in enumerate(universe) if all(ch == '.' for ch in row)]
    empty_cols = [c for c, col in enumerate(zip(*universe)) if all(ch == '.' for ch in col)]
    galaxies = [(r, c) for r, row in enumerate(universe) for c, ch in enumerate(row) if ch == '#']

    total = 0
    for (r1, c1), (r2, c2) in combinations(galaxies, 2):
        for r in range(min(r1, r2), max(r1, r2)):
            total += expansion if r in empty_rows else 1
        for c in range(min(c1, c2), max(c1, c2)):
            total += expansion if c in empty_cols else 1

    return total
```

The code is suspiciously similar to [someone else's][HyperNeutrino], with the
exception of using `itertools.combinations` for the galaxy pairs. The trick
of `zip`ping the rows and iterating over that to find the columns is neat,
but not as neat of [Clojure's transpose trick][so-clj-transpose] ;-)

Part one is `solve(universe, 2)` and Part two is `solve(universe, 1000000)`.

Day 12 - Hot Springs
--------------------

[Solution][d12-py] - [Back to top][top]

In day 12 we're trying to tell broken springs from good ones. Each line of
the input can be split in two parts: on the left each char represents one
spring, with `.` being a good one, `#` a damaged one and `?` meaning we don't
know. On the right we have some numbers, each one representing the length of
a contiguous block of damaged springs. With this information we can figure
out which of the `?` chars stand for good and bad springs and how many
possible configurations would match the right-hand side.

Parsing the input is trivial:

```python
def parse_input(data):
    parsed = []
    for line in data.splitlines():
        springs, groups = line.split()
        groups = tuple(map(int, groups.split(',')))
        parsed.append((springs, groups))
    return parsed
```

The problem can be solved by examining smaller configurations and building
up from them. The simplest cases are

- we've examined all the springs: the configuration is valid if there are
  no spring groups left to match
- we've matched all the spring groups: the configuration is valid if none
  of the remaining springs is broken

We're left with two possible cases:

- we're looking at a good spring or we're guessing that a `?` stands for
  a good spring: the configuration is valid if the remaining springs match
  all the groups
- we're looking at a bad spring or we're guessing that a `?` stands for a
  broken spring: the configuration is valid if either

  - we're left with just enough springs to examine to match the group we're
    examining: all of the remaining chars must be `#` or `?`
  - we're left with more springs than the group we're looking at: the
    configuration is valid only if the next chars are `#` or `?` and the
    one after them is a `.` because continuous groups must be separated
    by at least one good spring.

In every one of the above cases the solution of the problem is equal
to the solution of the same problem on a smaller string (the original
one minus the first `g` chars with `g` the number of springs in the first
group of springs) and the groups after the first. It also looks like
we'll be solving the same sub-problem again and again so some sort of
caching is in order. The code:

```python
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
```

Day 13 - Point of Incidence
---------------------------

[Solution][d13-py] - [Back to top][top]


In day 13 we're trying to find a subset of a grid that is reflects the same
pattern of `.` and `#` characters either horizontally along some row or
vertically along some column. The reflection needs not to be complete, for
example in the grid below only rows `(4, 5)`, `(3, 6)` and `(2, 7)` reflect
eacn other

```text
1 #...##..#
2 #....#..# v
3 ..##..### v
4 #####.##. v
5 #####.##. ^
6 ..##..### ^
7 #....#..# ^
```

For part one we want to find the row or column along which each grid in the
input reflectsc, summing `100` plus the row index for horizontal reflections
and just the column index for vertical ones. There's no parsing involved, we
just `split()` on `\n\n` to separate the grids and then try each row to see
if it's a possible reflection point. Note we start from row `1` since a valid
reflection it's made of at least two rows (`0` and `1` in this case)

```python
rows = grid.splitlines()
for r in range(1, len(rows)):
    total += 100 * r if is_reflection(rows, r) else 0
```

Checking for a reflection involves just finding out how many rows it would
cover and then comparing the rows

```python
def is_reflection(grid, row):
    size = min(row, len(grid) - row)
    return all(grid[row-i-1] == grid[row+i] for i in range(0, size))
```

Checking for reflections along a column... we don't want to do that, we'll
just flip the grid and reuse the row code:

```python
cols = [''.join(c) for c in zip(*rows)]
for c in range(1, len(cols)):
    total += c if is_reflection(cols, c) else 0
```

Putting it all together for part one we just need

```python
def part_1(data):
    total = 0
    for grid in data:
        rows = grid.splitlines()
        for r in range(1, len(rows)):
            total += 100 * r if is_reflection(rows, r) else 0

        cols = [''.join(c) for c in zip(*rows)]
        for c in range(1, len(cols)):
            total += c if is_reflection(cols, c) else 0
    return total
```

In part two we're told that on each grid there's exactly one row or column
that has one symbol that should be flipped from `.` to `#` or viceversa,
causing the reflection we're looking for to change. The code above still
works, we just need to update the function that checks for reflections:

```python
def is_reflection_pt2(grid, row):
    size = min(row, len(grid) - row)
    differences = 0
    for i in range(0, size):
        differences += sum(0 if a == b else 1 for a, b in zip(grid[row-i-1], grid[row+i]))
    return differences == 1
```

we're still checking a subset of rows but now we don't need all of them
to be exactly equal to their counterpart, we can tolerate a single error. We
can just sum `1` each time a symbol on two rows differs, and `0` when they're
equal. If after checking all the rows in the subset the total number of errors
is equal to `1` we've found the reflection we were looking for. Note that the
function for part two could be used for part one as well, only checking for
`0` errors instead of `1`.


Day 14 - Parabolic Reflector Dish
---------------------------------

[Solution][d14-py] - [Back to top][top]

In day 14 we're tilting a dish with some rocks on it: the rocks `O` will roll
until they reach the edge of the dish or a square rock `#`. After the rocks
have reached they resting position we can calculate the load they put on the
top side of the dish by adding `n` points for each rock on a single line,
with `n` being the distance of the rock from the bottom side.

In part 1 we're asked to just tillt the dish north, so all rocks will roll
to the top. Dealing with left-to-right strings is much easier than working
with grid columns, so we'll just transpose the initial grid:

```python
def transpose(grid):
    return tuple(''.join(column) for column in zip(*grid))
```

Rocks will either roll all to the left or to the right until they reach an
edge or a `#` character. We can split the problem of rolling all the rocks
on a line on the simpler problem of moving all rocks to the left or to the
right of the spans between an edge and a `#` or between `#`s

```python
def roll_left(rocks):
    return ''.join(sorted(rocks, reverse=True))

def roll_right(rocks):
    return ''.join(sorted(rocks))
```

Tilting the dish to the north then is just

```python
def tilt_north(dish):
    cols = transpose(dish)
    tilted = tuple('#'.join([roll_left(span) for span in c.split('#')]) for c in cols)
    return transpose(tilted)
```

and part 1 is simply

```python
def part_1(dish):
    return sum(line.count('O') * (len(dish) - i) for i, line in enumerate(tilt_north(dish)))
```

In part 2 we want to repeat a single cycle of tilting the dish nort, west, south
and then east for a ludicrous number of times. We'll need

```python
def tilt_west(dish):
    return tuple('#'.join([roll_left(span) for span in row.split('#')]) for row in dish)

def tilt_south(dish):
    cols = transpose(dish)
    tilted = tuple('#'.join([roll_right(span) for span in c.split('#')]) for c in cols)
    return transpose(tilted)

def tilt_east(dish):
    return tuple('#'.join([roll_right(span) for span in row.split('#')]) for row in dish)

def spin(dish):
    dish = tilt_north(dish)
    dish = tilt_west(dish)
    dish = tilt_south(dish)
    dish = tilt_east(dish)
    return dish
```

but then calling `spin` for a trillion will take a while. **Surely** some rock
configuration will repeat, so if we just determine the initial configuration of
a loop and the loop length we'll cut down the time to reach the trillionth
configuration

```python
def part_2(dish):
    seen = {dish}
    steps = [dish]

    iterations = 0
    while True:
        iterations += 1
        dish = spin(dish)
        if dish in seen:
            break
        seen.add(dish)
        steps.append(dish)

    loop_start = steps.index(dish)
    loop_size = iterations - loop_start
    result = steps[loop_start + (1000000000 - loop_start) % loop_size]

    return sum(line.count('O') * (len(result) - i) for i, line in enumerate(result))
```


Day 15 - Lens Library
---------------------

[Solution][d15-py] - [Back to top][top]

In day 15 we're re-inventing hashing. Part one wants us to calculate the sum of
the comma separated parts of the input:

```python
def HASH(step):
    return reduce(lambda acc, c: ((acc + ord(c)) * 17) % 256, step, 0)

def part_1(init_sequence):
    return sum(HASH(s) for s in init_sequence.split(','))
```

Part two explains what the parts in the input text are: instructions on
adding and removing lenses from boxes: each instruction is made of a label,
followed by a `-` sign or an `=` sign and a number. The `-` removes the
lens labeled from the box indicated by the hash code of the label. The `=`
labels a lens of the given focal length with the instruction label and puts
it in the box indicated by the hash of the label.

```python
def add_lens(box, label, focal_length):
    box[label] = focal_length

def remove_lens(box, label):
    if label in box:
        del box[label]

def part_2(init_sequence):
    boxes = [dict() for _ in range(256)]
    for step in init_sequence.split(','):
        label, focal_length = re.split(r'[-=]', step)
        if focal_length:
            add_lens(boxes[HASH(label)], label, int(focal_length))
        else:
            remove_lens(boxes[HASH(label)], label)
    total = 0
    for i, box in enumerate(boxes, 1):
        for j, label in enumerate(box, 1):
            total += i * j * box[label]
    return total
```

Day 16 - The Floor Will Be Lava
-------------------------------

In day 16 we will be tracing the path of a ray of light as it travels on
a grid interacting with some mirrors and splitters. The ray of light enters
the grid in the top-left corner going right and will keep traveling in that
direction unless diverted by an angled mirror or split by a splitter. We can
map the direction the beam travels to a tuple of row and column differences:

```python
DELTAS = {
    'U': (-1, 0), 'D': (1, 0), 'R': (0, 1), 'L': (0, -1)
}
```

and then the rules that determine how the beam interacts with the objects
on the grid cells

```python
BEAM_DESTINATIONS = {
    '.':  { 'R': 'R', 'L': 'L', 'U': 'U', 'D': 'D' },
    '|':  { 'R': 'UD', 'L': 'UD', 'U': 'U', 'D': 'D' },
    '-':  { 'R': 'R', 'L': 'L', 'U': 'LR', 'D': 'LR' },
    '\\': { 'R': 'D', 'L': 'U', 'U': 'L', 'D': 'R' },
    '/':  { 'R': 'U', 'L': 'D', 'U': 'R', 'D': 'L' },
}
```

For part 1 we want to know how many grid cells the beam will visit (note that
the beam could pass the same coordinates more than once). We can do that by
keeping track of what grid position the beam is on and which direction it's
traveling to determine the next cell it will visit. The beam will split when
hitting a splitter head-on so we'll need a queue of the paths we haven't
yet considered:

```python
def traverse(grid, height, witdth, start=(0, 0, 'R')):
    visited = set()
    to_visit = deque()
    to_visit.append(start)
    while to_visit:
        row, col, direction = to_visit.popleft()
        if (row, col, direction) in visited:
            continue
        visited.add((row, col, direction))
        for dst in BEAM_DESTINATIONS[grid[row][col]][direction]:
            dr, dc = DELTAS[dst]
            if 0 <= row + dr < height and 0 <= col + dc < witdth:
                to_visit.append((row+dr, col+dc, dst))
    return len({(r, c) for r, c, _ in visited})

def part_1(grid):
    height = len(grid)
    width = len(grid[0])
    return traverse(grid, height, width)
```

note that for keeping track of the visited cells we're using a set, speeding
up lookups.

For part 2 we're told the beam of light could enter the grid from any of the
cells on the edges, and we want to know which of those will maximize the
number of cells it traverses. Part 1 should be fast enough (if you use a
`set` ;-)) to brute force part 2:

```python
def part_2(grid):
    height = len(grid)
    width = len(grid[0])
    max_energy = 0
    for r in range(height):
        max_energy = max(max_energy, traverse(grid, height, width, (r, 0, 'R')))
        max_energy = max(max_energy, traverse(grid, height, width, (r, width - 1, 'L')))
    for c in range(width):
        max_energy = max(max_energy, traverse(grid, height, width, (0, c, 'D')))
        max_energy = max(max_energy, traverse(grid, height, width, (height-1, c, 'U')))
    return max_energy
```


Notes
-----

<sup>†</sup> The solution for part 2 is _heavily_ inspired by [HyperNeutrino].


---
[top]: #advent-of-code-2023

[d01]: #day-1---trebuchet
[d02]: #day-2---cube-conundrum
[d03]: #day-3---gear-ratios
[d04]: #day-4---scratchcards
[d05]: #day-5---if-you-give-a-seed-a-fertilizer
[d06]: #day-6---wait-for-it
[d07]: #day-7---camel-cards
[d08]: #day-8---haunted-wasteland
[d09]: #day-9---mirage-maintenance
[d10]: #day-10---pipe-maze
[d11]: #day-11---cosmic-expansion
[d12]: #day-12---hot-springs
[d13]: #day-13---point-of-incidence
[d14]: #day-14---parabolic-reflector-dish
[d15]: #day-15---lens-library
[d16]: #day-16---the-floor-will-be-lava
[notes]: #notes

[d01-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_01.py
[d02-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_02.py
[d03-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_03.py
[d04-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_04.py
[d05-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_05.py
[d06-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_06.py
[d07-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_07.py
[d08-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_08.py
[d09-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_09.py
[d10-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_10.py
[d11-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_11.py
[d12-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_12.py
[d13-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_13.py
[d14-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_14.py
[d15-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_15.py
[d16-py]: https://github.com/agnul/AdventOfCode/blob/main/2023/python/day_16.py

[HyperNeutrino]: https://www.youtube.com/playlist?list=PLnNm9syGLD3zLoIGWeHfnEekEKxPKLivw
[wiki-lcm]: https://en.wikipedia.org/wiki/Least_common_multiple
[wiki-bfs]: https://en.wikipedia.org/wiki/Breadth-first_search
[wiki-picks]: https://en.wikipedia.org/wiki/Pick's_theorem
[wiki-shoelace]: https://en.wikipedia.org/wiki/Shoelace_formula
[wiki-taxicab]: https://en.wikipedia.org/wiki/Taxicab_geometry
[so-clj-transpose]: https://stackoverflow.com/a/10347404/6069
