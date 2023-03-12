Advent of Code 2022
===================

Advent of code 2022 done in Clojure. I don't (yet?) know anything about
Clojure and my only exposure to functional programming comes from way
back in school and the streams and lambdas in java 8. How far will I get?


Table of contents
-----------------

- [Day 1 - Calorie Counting][d01]
- [Day 2 - Rock Paper Scissors][d02]
- [Day 3 - Rucksack Reorganization][d03]
- [Day 4 - Camp Cleanup][d04]
- [Day 5 - Supply Stacks][d05]


Day 1 - Calorie Counting
------------------------

[Solution][d01-clj] - [Back to top][top]

We are given a list of number groups, each group separated from the others
with a blank line, each number on its own line. For part one we have to find
the largest sum of the numbers in a block.

We start parsing the input: we [read the whole][docs-slurp] file and split
on blank lines

```clojure
(defn parse-input
  [filename]
  (mapv parse-meal (str/split (slurp filename) #"\n\n")))
```

and for each line in the groups we read we apply `Long/parseLong` to
obtain numbers. On older versions of Clojure we resort to the static
method `java.lang.Long.parseLong` in an anoymous function since there's
no `parse-long` in `core` and Java interop is like that `¯\_(ツ)_/¯`


```clojure
(defn parse-meal
  [lines]
  (mapv #(Long/parseLong %) (str/split lines #"\n")))
```

We now want to sum the numbers of each group and then the highest
sum, so we first map `#(reduce + %)` to get a vector of sums

```clojure
(let [meals (parse-input filename)]
  (mapv #(reduce + %) meals))
```

... and then get the highest value by [applying][docs-apply] `max`

```clojure
(let [meals (parse-input filename)]
    (apply max (mapv #(reduce + %) meals)))
```

For part two we want the sum of the top three groups, so we sum numbers
like before, sort in decreasing order...

```clojure
(let [meals (parse-input filename)
      calories (mapv #(reduce + %) meals)]
  (sort > calories))
```

... take the first three values and sum them.

```clojure
(let [meals (parse-input filename)
      calories (mapv #(reduce + %) meals)]
  (reduce + (take 3 (sort > calories))))
```


Day 2 - Rock Paper Scissors
---------------------------

[Solution][d02-clj] - [Back to top][top]

We are given a list of _instructions_ to follow when playing a game
of rock, paper, scissors. Each line of the input files has two letters
separated by a blank. The first letter is one of `A`, `B`, `C`,
respectively for Rock, Paper or Scissors. Likewise the second letter is
one of `X`, `Y`, `Z`. Each one of Rock, Paper and Scissors has a score:
`1` for Rock, `2` for Paper and `3` for Scissors. For each round we
gain `0` points if we loose, `3` for a draw and `6` for a win.

Since the input is so simple we won't bother with parsing and we'll just
take each line and map it to a score. For part one we want the total score
after all the rounds are played, and the score is calculated as the sum of
the round result and the value of the symbol we'll play, e.g. for `A X`
our opponent will play Rock (`A`) and we'll play Rock as well (`X`); the
resulting soore will be `4` points, `3` because the round is a draw and
`1` because we play Rock.

```clojure
(let [scores
      {"A X" (+ 3 1) "A Y" (+ 6 2) "A Z" (+ 0 3)
       "B X" (+ 0 1) "B Y" (+ 3 2) "B Z" (+ 6 3)
       "C X" (+ 6 1) "C Y" (+ 0 2) "C Z" (+ 3 3)}]
  ...  
  )
```

we'll just need to match each line to the corresponing score and sum
all the values

```clojure
(defn part-1
  [input]
  (let [scores
        {"A X" (+ 3 1) "A Y" (+ 6 2) "A Z" (+ 0 3)
         "B X" (+ 0 1) "B Y" (+ 3 2) "B Z" (+ 6 3)
         "C X" (+ 6 1) "C Y" (+ 0 2) "C Z" (+ 3 3)}]
    (->> (str/split input #"\n")
         (map #(get scores %))
         (reduce +))))
```

Part two is almost identical to part one, but this time each line of the
input tells us what our opponent will play and the desired outcome of the
round, `X` for a loss, `Y` for a draw and `Z` for a win. Again, each line
has a score, e.g. for `A X` our opponent will play Rock and we want a loss,
so we'll play Scissors, resulting in `3` points for playing Scissors and
`0` points for a loss.

```clojure
(defn part-2
  [input]
  (let [scores 
        {"A X" (+ 3 0) "A Y" (+ 1 3) "A Z" (+ 2 6)
         "B X" (+ 1 0) "B Y" (+ 2 3) "B Z" (+ 3 6)
         "C X" (+ 2 0) "C Y" (+ 3 3) "C Z" (+ 1 6)}]
    (->> (str/split input #"\n")
         (map #(get scores %))
         (reduce +))))
```


Day 3 - Rucksack Reorganization
-------------------------------

[Solution][d03-clj] - [Back to top][top]

We are given a list of strings of lower and uppercase letters. For part
one we are told that the letters in each string are all different except
for one that appears in both the first and the second half of the string.
For each of the strings we must find the one repeated letter, assign it
a value and take the sum of all the found values. Letters `a` to `z`
have values `1` to `26`, `A` to `Z` are `27` to `52`.

Reading the input is trivial: `slurp` the file, split on newlines and
turn each line into a [sequence][docs-seq] of characters.

```clojure
(defn read_input
  [filename]
  (map seq (str/split (slurp filename) #"\n")))
```

We need to tell if a charater is upper or lower case, and to do so
we convert the character to an integer and check that the resulting
number is between the values of `A` and `Z`

```clojure
(defn is_upper?
  [letter]
  (<= (int \A) (int letter) (int \Z)))
```

With that we can calculate the score of each character: for upper
case characters we subtract `A`, which results in a number between
`0` for `A` and `25`for `Z`, and since we need scores from `27` to
`52` we add `27`. For lowercase characters we subtract `a` and add
`1`

```clojure
(defn score
  [letter]
  (cond
    (is_upper? letter) (+ 27 (- (int letter) (int \A)))
    :else              (+  1 (- (int letter) (int \a)))))
```

To find the character that is common to the two halves of a sequence
we split it in two and convert each half into a [`set`][docs-set] and
take the [intersection][docs-intersection] of the two


```clojure
(defn find-misplaced-item
  [rucksack]
  (let [half (/ (count rucksack) 2)
        first-half (set (take half rucksack))
        second-half (set (drop half rucksack))]
    (first (set/intersection first-half second-half))))
```

Putting it all together we can solve part one

```clojure
(defn part-1
  [filename]
  (let [rucksacks (read_input filename)]
    (->> rucksacks
         (map find-misplaced-item)
         (map score)
         (reduce +))))
```

For part two we are asked to split the initial list in groups of three
elements

```clojure
(let [elf-groups (partition 3 (map set (read_input filename)))]
    ...)
```

and then find the one letter that is commont to all of them.

```clojure
(defn find-badge
  [group]
  (map first (map #(apply set/intersection %) group)))
```

As for part one we assign a score to the letter we found and sum the
scores of each group

 ```clojure
 (defn part-2
  [filename]
  (let [elf-groups (partition 3 (map set (read_input filename)))]
    (->> elf-groups
         (find-badge)
         (map score)
         (reduce +))))
```


Day 4 - Camp Cleanup
-------------------

[Solution][d04-clj] - [Back to top][top]

We're given a list of integer ranges, two to a line. We start with parsing:
each line has the form

```text
a-b,c-d
```

with `a`, `b`, `c` and `d` integer numbers. We don't need nothing fancy,
just read the whole file, split the string on newlines, dashes and commas
and divide the resulting numbers in groups of four

```clojure
(defn read_input
  [filename]
  (partition 4 (map parse-long (str/split (slurp filename) #"[\n,-]"))))
```

For part one we want to know for how many of them one of the two is
fully contained in the other, so it's either one of the two cases

```text
A----------B      C----------D
   C-------D        A-------B
```

Note that `A` could be equal to `C` and `B` to `D`.

We can express the above with the function

```clojure
(defn fully_contained?
  [a b c d]
  (or (<= a c d b) (<= c a b d)))
```

And just count how many ranges are left after filtering the original
list

```clojure
(defn part-1
  [filename]
  (->> (read_input filename)
       (filter #(apply fully_contained? %))
       (count)))
```

For part two we want to know how many ranges overlap. Two ranges
overlap if one fully contains the other or either of the two is
true

```text
A----------B            A----------B
       C-------D      C-------D

```

Again `C` could be equal to `B`.

We just define

```clojure
(defn overlapping?
  [a b c d]
  (or (fully_contained? a b c d)
      (<= a c b d)
      (<= c a d b)))
```

and swap it the `part-1` function

```clojure
(defn part-2
  [filename]
  (->> (read_input filename)
       (filter #(apply overlapping? %))
       (count)))
```


Day 5 - Supply Stacks
---------------------

[Solution][d05-clj] - [Back to top][top]

We're given an input in two parts: the first is a drawing of stacked boxes,
the second is a list of instructions for moving boxes around. As usual we
slurp the whole file in a string, then we parse the two parts separately.

For the "instructions" part we're only interested in the three numbers in
each input line, so we can just use a regex to match one or more digits
all over the second part of the input, applying `parse-long` and
partitioning the resulting list every three elements.

```clojure
(defn read-input
  [filename]
  (let [[stacks instructions] (str/split (slurp filename) #"\n\n")]
    {:stacks (read-stacks stacks)
     :instructions (->> instructions
                        (re-seq #"\d+")
                        (map parse-long)
                        (partition 3))}))
```

Parsing the stacks is trickier. The simple way would be to split the
first part of the input into lines, transpose the resulting list and read
the stacks every matching the `A..Z` characters

```text
    [D]             [N] [Z]      (\N \Z)
[N] [C]      => [D] [C] [M]  =>  (\D \C \M)
[Z] [M] [P]             [P]      (\P)
```

but silly old me decided for the complicated way: figure on wich columns
are the alphabetic characters in the input (2nd, 6th, 10th...) and read
the input char at given columns on each line, returning a list of "stacks".
Easier said (?) than done.

We start with `read-stacks`: it figures out how long each input line is and
how many charaters need to be skipped to get to the next element in each
colum (that's `line-lenght + 1`, as each line ends with a `\newline`) and
then loops until the last column calling `read-stack` to build a list of
stacks. Since `conj` adds new elements to a list at the head position we
need to reverse the list of stacks when we're finished.

```clojure
(defn read-stacks
  [input]
  (let [line-length (str/index-of input \newline) 
        mod (+ 1 line-length)]
    ; start with a dummy stack at position zero
    ; so we don't have to fix indexes in instructions
    (loop [i 1 stacks '((\0))]
      (if-not (< i line-length)
        (reverse stacks)
        (recur (+ i 4) (conj stacks (read-stack input i mod)))))))
```

`read-stack` works pretty similarly: we start on the first element of each
column and call `push-crate` to add the characters into a stack, until we
run out of input. As for `read-stacks` we're building the stack backwars, 
so we need to reverse it before returning.

```clojure
(defn read-stack
  [input column mod]
  (loop [offset column stack ()]
    (if-not (< offset (count input))
      (reverse stack)
      (recur (+ offset mod) (push-crate (nth input offset) stack)))))
```

`push-stack` simply adds a new character to the head of a list, filtering
out the blanks.

```clojure
(defn push-crate
  [crate stack]
  (if-not (= crate \space)
    (conj stack crate)
    stack))
```

At the end of all that we're left with a list of stacks (each one a list of
characters) and a list of instructions (each one a list of three numbers).
Note that we have an extra empty stack at the start so we don't need to fix
the commands (list elements start at index `0`, the instructions we're given
assume stacks start at `1`) and that at the eand of each stack we left an
extra character that identifies the stack: that will be useful later (?).
The problem ask us to move crates between stacks, with each line in the
instrcutions made of a number of crates, the stacks to move them from and.
the destination, e.g. `(3 1 3)` meaning move three crates from stack number
one to stack number three. For part one we move crates one at a time, so the
above means repeating three times a single crate move from stack one to
stack thee. To move a single crate all we need to do is `replace` the origin
stack with a new one without its first element and the destination stack
with a one with the moved element on top.

```clojure
(defn move-one-crate
  [stacks from to]
  (let [from-stack (nth stacks from)
        to-stack (nth stacks to)
        crate (first from-stack)]
    (replace {from-stack (rest from-stack)
              to-stack (conj to-stack crate)} stacks)))
```

To repeat one move `times` times we just loop 

```clojure
(defn with-crate-master-9000
  [stacks times from to]
  (loop [i 0 res stacks]
    (if-not (< i times)
      res
      (recur (inc i) (move-one-crate res from to)))))
```

and to apply all the instructions in the file we just pass the above
function to `move-stacks-in`

```clojure
(defn move-stacks-in
  [filename move-fn]
  (let [{:keys [stacks instructions]}
        (read-input filename)]
    (loop [moves instructions res stacks]
      (if (empty? moves)
        res
        (recur (rest moves) (apply move-fn res (first moves)))))))
```

Note that moving the crates one at a time means that when moving multiple
crates they land on the destination in reverse order.

After all the moves are done we want to know what word the top of each stack
spells (note that we drop the first dummy stack)

```clojure
(defn top-of-stacks
  [stacks]
  (->> stacks
       (map first)
       (drop 1)
       (apply str)))
```

Wrapping it all up for part one:

```clojure
(defn part-1
  [filename]
  (top-of-stacks (move-stacks-in filename with-crate-master-9000)))
```

In part two we do the same, but this time we move all the crates at once.
We can reuse all of the above and just create a new function to pass to
`move-stacks-in` (I still haven't figure out the whole `cons`, `conj` and
`into` stuff)

```clojure
(defn with-crate-master-9001
  [stacks cnt from to]
  (let [from-stack (nth stacks from)
        to-stack (nth stacks to)
        crates (take cnt from-stack)]
    (replace {from-stack (drop cnt from-stack)
              to-stack (into to-stack (reverse crates))} stacks)))
```

and then it's just

```clojure
(defn part-2
  [filename]
  (top-of-stacks (move-stacks-in filename with-crate-master-9001)))
```

---
[top]: #advent-of-code-2022

[d01]: #day-1---calorie-counting
[d02]: #day-2---rock-paper-scissors
[d03]: #day-3---rucksack-reorganization
[d04]: #day-4---camp-cleanup
[d05]: #day-5---supply-stacks


[d01-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_01.clj
[d02-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_02.clj
[d03-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_03.clj
[d04-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_04.clj
[d05-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_05.clj


[docs-slurp]: https://clojuredocs.org/clojure.core/slurp
[docs-apply]: https://clojuredocs.org/clojure.core/apply
[docs-seq]: https://clojuredocs.org/clojure.core/seq
[docs-set]: https://clojuredocs.org/clojure.core/set
[docs-intersection]: https://clojuredocs.org/clojure.set/intersection
