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
- [Day 6 - Tuning Trouble][d06]
- [Day 7 - No Space Left On Device][d07]
- [Day 8 - Treetop Tree House][d08]
- [Day 9 - Rope Bridge][d09]
- [Day 10 - Cathode-Ray Tube][d10]
- [Day 11 - Monkey in the Middle][d11]<sup>†</sup>
- [Day 12 - Hill Climbing Algorithm][d12]
- [Day 13 - Distress Signal][d13]<sup>‡</sup>
- [Day 14 - Regolith Reservoir][d14]
- [Day 15 - Beacon Exclusion Zone][d15]
- [Notes][notes]


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
      (if (< i line-length)
        (recur (+ i 4) (conj stacks (read-stack input i mod)))
        (reverse stacks)))))
```

`read-stack` works pretty similarly: we start on the first element of each
column and call `push-crate` to add the characters into a stack, until we
run out of input. As for `read-stacks` we're building the stack backwards,
so we need to reverse it before returning.

```clojure
(defn read-stack
  [input column mod]
  (loop [offset column stack ()]
    (if(< offset (count input))
      (recur (+ offset mod) (push-crate (nth input offset) stack))
      (reverse stack))))
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
    (if (< i times)
      (recur (inc i) (move-one-crate res from to))
      res)))
```

and to apply all the instructions in the file we just pass the above
function to `move-stacks-in`

```clojure
(defn move-stacks-in
  [filename move-fn]
  (let [{:keys [stacks instructions]}
        (read-input filename)]
    (loop [moves instructions res stacks]
      (if-not (empty? moves)
        (recur (rest moves) (apply move-fn res (first moves)))
        res))))
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


Day 6 - Tuning Trouble
----------------------

[Solution][d06-clj] - [Back to top][top]

For day 6 we're given a string and we want to find at what location in the
string a sequence of four unique chars ends. Readint input is a simple
`slurp`. After that we want a function telling us if the last `size` chars
at offset `offset` in the string `stream` are unique:

```clojure
(defn has-received-marker?
  [stream offset size]
  (let [packet (subs stream (- offset size) offset)]
    (= size (count (set packet)))))
```

and then we can just iterate every possible offset until we find what we're
looking for

```clojure
(defn find-marker
  [stream size]
  (loop [offset size]
    (cond
      (has-received-marker? stream offset size) offset
      (> offset (count stream))                 nil
      :else                                     (recur (inc offset)))))
```

For part two we're asked the same thing, but now we're looking for 14 unique
chars.

Day 7 - No Space Left On Device
-------------------------------

[Solution][d07-clj] - [Back to top][top]

In day 7 we're given the transcript of a terminal session made of commands
and their output. Command lines begin with a `$` sign, output lines are
either a number and a name (representing a file and its size) or the
string `dir` followed by a name (representing a directory).

For part one we want to find which directories have a total size of at
most 100000, so we'll need to figure out the filesystem state from the
terminal output. We could build a map of pathnames to sizes... or we could
rebuild the filesystem tree! Our tree nodes will contain a name, a size
and an optional map of names to other nodes, representing the current
node's children:

```clojure
(defn mknode
  [line]
  (let [[size name] (str/split line #"\s+")]
    (if (= "dir" size)
      {:name name :size 0}
      {:name name :size (parse-long size) :children {}})))
```

Then we'll need to append new nodes to existing ones

```clojure
(defn append
  [root cwd {:keys [name size]:as node}]
  (let [[dir & dirs] cwd
        parent (get-in root [:children dir])]
    (if-not (empty? cwd)
      (-> root
          (update :size + size)
          (assoc-in [:children dir] (append parent dirs node)))
      (-> root
          (update :size + size)
          (assoc-in [:children name] node)))))
```

With all that in place we can rebuild the tree simply checking each line
in the transcript: if it's a command we'll just _run_ it, otherwise we
append a new node in the filesystem tree. We'll need to keep track of the
state as we build, so we'll use a simple map like
`{:root file-system :cwd []}`

Putthing it all together

```clojure
(defn is-command?
  [line]
  (str/starts-with? line "$"))

(defn execute-cmd
  [state cmd-line]
  (let [[_ cmd arg] (str/split cmd-line #"\s+")]
    (if (= cmd "cd")
      (condp = arg
        "/"  (assoc state :cwd [])
        ".." (update state :cwd pop)
        (update state :cwd conj arg))
      state)))

(defn add-file-or-dir
  [{:keys [root cwd] :as state} line]
  (assoc state :root (append root cwd (mknode line))))

(defn make-tree
  [terminal-output]
  (:root
   (reduce
    (fn [state line]
      (if (is-command? line)
        (execute-cmd state line)
        (add-file-or-dir state line)))
    {:root (mknode "dir /") :cwd []}
    terminal-output)))

(defn read-input
  [filename]
  (->> filename
       slurp
       str/split-lines
       make-tree))
```

We are now ready to solve our problem: look for directories in the tree
(they're the nodes that have the `:children` key), keep the ones smaller
than 100000, sum their sizes.

```clojure
(defn sub-dirs
  [dir]
  (filter #(contains? % :children) (vals (:children dir))))

(defn dir-sizes
  [dir]
  (let [size (:size dir)
        subs (sub-dirs dir)]
    (if-not (empty? subs)
      (conj (flatten (map dir-sizes subs)) size)
      size)))

(defn part-1
  [filename]
  (let [root (read-input filename)]
    (->> root
         dir-sizes
         (filter #(< % 100000))
         (reduce +))))
```

For part two we get to reuse most of the above: our device has a total
capacity of 7'000'0000 and we need at least 3'000'0000 of free space.
Part two asks what is the smallest subdir we must delete to achieve that

```clojure
(defn part-2
  [filename]
  (let [root (read-input filename)
        free (- 70000000 (:size root))
        goal (- 30000000 free)]
    (->> root
         dir-sizes
         (filter #(>= % goal))
         (reduce min))))
```

Day 8 - Treetop Tree House
--------------------------

[Solution][d08-clj] - [Back to top][top]

In day 8 we start with a grid of numbers. We can parse that splitting the
input into lines, splitting each line into single digit strings and parse
those string, reassembling everything into a vector. We'll be needing the
grid width, so we take note of the lenght of the first row, and since the
problems will have us going into the grid both horizontally and vertically
we'll also rearrange the input into columns.

```clojure
(defn parse-input
  [string]
  (let [lines (str/split-lines string)
        rows (mapv #(mapv parse-long (str/split % #"")) lines)
        columns (apply mapv vector rows)
        size (count (first rows))]
    {:rows rows :columns columns :size size}))
```

Part one wants us to count how many of the numbers are "visible" from the
edges of the grid, meaning that there are no numbers on its left, right,
top or bottom that are greater than or equal to it. Let's start checking
that a numnber at row `r` and column `c` is visile. We can split each row
(or column) three parts. Consider the number `5` at position `(1, 2)`
(second row, third column, counting from `0`)

```text
         c
   3 0  (3)  7 3
r (2 5)  5  (1 2)
   6 5  (3)  3 2
   3 3  (5)  4 9
   3 5  (3)  9 0
```

the numbers on the left are just `(take 2 row)`, or more specifically
`(take 2 (nth rows 1))`, those on it's right are `(drop 3 row)` or,
more specifically, `(drop (inc 2) (nth rows 1))`. Same goes for the
numbers above and below, respectively `(take 1 (nth columns 2))` and
`(drop (inc 1) (nth columns 2))`. Putting it all together we have

```clojure
(defn visible?
  [{:keys [rows columns]} r c]
  (let [it (nth (nth rows r) c)
        left (take c (nth rows r))
        right (drop (inc c) (nth rows r))
        top (take r (nth columns c))
        bottom (drop (inc r) (nth columns c))]
    (or (every? #(> it %) left)
        (every? #(> it %) right)
        (every? #(> it %) top)
        (every? #(> it %) bottom))))
```

We can now solve part one iterating over the grid and counting for how
many of those the above function is true.

```clojure
(defn part-1
  [filename]
  (let [data (->> filename slurp parse-input)
        size (:size data)]
    (count (filter true?
                   (for [r (range size)
                         c (range size)]
                     (visible? data r c))))))
```

Part two wants us to calculate a score for each position on the grid and
find the highest score. To find the score at position `(r, c)` we want to
count how many numbers on the left, right, top and bottom are smaller or
equal to the one at that position, _stopping counting at the first one
that is greater_. Given a list of numbers we can count how many of them
satisfy the above condition with the function

```clojure
(defn count-visible
  [[t & ts]]
  (:cnt
   (reduce
    (fn [{:keys [cnt done] :as state} h]
      (cond
        (and (not done) (> t h))
        {:cnt (inc cnt) :done false}

        (not done)
        {:cnt (inc cnt) :done true}

        :else
        state))
    {:cnt 0 :done false} ts)))
```

with that the score of any position can be calculated with

```clojure
(defn score
  [{:keys [rows columns]} r c]
  (let [left (take (inc c) (nth rows r))
        right (drop c (nth rows r))
        top (take (inc r) (nth columns c))
        bottom (drop r (nth columns c))
        v1 (count-visible (reverse left))
        v2 (count-visible right)
        v3 (count-visible (reverse top))
        v4 (count-visible bottom)]
    (* v1 v2 v3 v4)))
```

and part two is solved with

```clojure
(defn part-2
  [filename]
  (let [data (->> filename slurp parse-input)
        size (:size data)]
    (apply max (for [r (range size)
                     c (range size)]
                 (score data r c)))))
```

Day 9 - Rope Bridge
-------------------

[Solution][d09-clj] - [Back to top][top]

In day 9 we're simulating the movemnts of a "rope", made initially of two
"knots" that we'll call _head_ and _tail_. We are told that head and tail
must always touch, either horizontally, vertically or diagonally (if head
and tail overlap that counts as touching). As soon as the head is two
steps away horizontally or vertically the tail moves one step in the
direction of the head. If the head and tail are not touching and are not
horizontally or vertically aligned then the tail moves one step diagonnaly
towards the heead.

Our input contains the head's movements, one per line. We are told that
head and tail start at the same position and we must count how many
distinct positions the tail will visit following the head as it moves.

We start parsing the input: read the input string, split lines and turn
each line into a pair like `(direction, count)`

```clojure
(defn parse-move
  [string]
  (let [[direction cnt] (str/split string #"\s")]
    (list (keyword direction) (parse-long cnt))))

(defn parse-input
  [input]
  (->> input
       str/split-lines
       (map parse-move)))
```

We'll be representing the knots as a vector `[x  y]`  of coordinates and
the rope as a list of knots, so we'll need two utility functions for
adding and subtracting two vectors

```clojure
(defn add
  [[x0 y0] [x1 y1]]
  [(+ x0 x1) (+ y0 y1)])

(defn sub
  [[x0 y0] [x1 y1]]
  [(- x0 x1) (- y0 y1)])
```

then another one for deciding in which direction the head will move

```clojure
(defn delta
  [n1 n2]
  (let [[dx dy] (sub n1 n2)]
    [(if-not (zero? dx) (/ dx (abs dx)) 0)
     (if-not (zero? dy) (/ dy (abs dy)) 0)]))
```

and a last one for deciding if the tail needs to move

```clojure
(defn tail-moves?
  [[hx hy] [tx ty]]
  (or (> (abs (- hx tx)) 1)
      (> (abs (- hy ty)) 1)))
```

Moving a single knot **one step** in a given direction is done by just
adding the `[dx dy]` vector corresponding to the direction

```clojure
(defn move-knot
  [knot direction]
  (let [deltas {:U [0 1], :D [0 -1], :L [-1 0], :R [1, 0]}]
    (add knot (direction deltas))))
```

Moving the tail after the head has moved is done by

```clojure
(defn move-tail
  [head tail]
  (if (tail-moves? head tail)
    (add tail (delta head tail))
    tail))
```

and moving the whole rope **one step** in a given direction is done
repeating the two steps above on each pair of knots in the rope (and
keeping track of the positions occupied by the tail after each move)

```clojure
(defn move-rope
  [{:keys [rope visited]} direction]
  (let [moved (reduce
               (fn [head tail]
                 (conj head (move-tail (peek head) tail)))
               [(move-knot (first rope) direction)]
               (rest rope))]
    {:rope moved, :visited (conj visited (peek moved))}))
```

To solve the problem for a rope of any size we just iterate over the
instructions in the input, repeat for each line the single step
`move-rope` the desired amount of times, and count how many positions
have been saved in the `visited` set.

```clojure
(defn solve
  [size instructions]
  (->> instructions
       (reduce
        (fn [state [direction times]]
          (nth (iterate #(move-rope % direction) state) times))
        {:rope (repeat size [0 0]), :visited #{[0 0]}})
       :visited
       count))
```

For part one the rope is made of just the head and the tail

```clojure
(defn part-1
  [input]
  (solve 2 input))
```

while for part two the rope is make of ten knots

```clojure
(defn part-2
  [input]
  (solve 10 input))
```

Day 10 - Cathode-Ray Tube
-------------------------

[Solution][d10-clj] - [Back to top][top]

In day 10 we're given a list of instructions for a device with a screen.
Each instructions is either a no-operation (`noop`) or an addition to the
only register available on the device's CPU (`addx`). No-op instructions
leave the value of the register unchanged and take one clock cycle to run,
wihle add instructions add the value given as an argument to the
instrcution to the current value of the register and take two clock
cycles to run. That means that the value of the register only changes at the end of the second cycle of the instructions.

We start parsing the input:

```clojure
(defn parse-opcode
  [line]
  (let [[op arg] (str/split line #"\s+")]
    (if-not (= op "noop") (parse-long arg) 0)))

(defn parse-input
  [input]
  (->> input
       str/split-lines
       (mapv parse-opcode)))
```

Note that we're cheating: we represent instructions as integers, with `0`
being `noop`. That only works if the arguments to `addx` are always non
zero. Problem input seems to satisfy that condition... or maybe we're just
lucky.

Part one we wants us to sample the value of the register on the 20th clock
cycle and every 40 cycles after that, and then to multiply that number by the clock cycle. We need to `run` the program and collect the values of
the register at each clock cycle

```clojure
(defn collect-x-values
  [opcodes]
  (reduce
   (fn [x-values op-arg]
     (let [prev (peek x-values)]
       (if-not (zero? op-arg)
         (conj (conj x-values prev) (+ prev op-arg))
         (conj x-values prev))))
   [1] opcodes))
```

and then we can sample the value at a given clock with

```clojure
(defn sample-strength
  [x-values clock]
  (* clock (nth x-values (dec clock))))
```

At last we can solve part one with

```clojure
(defn part-1
  [input]
  (let [opcodes (parse-input input)
        x-values (collect-x-values opcodes)
        max-clock (count x-values)
        sample-times (range 20 max-clock 40)]
    (->> sample-times
         (map #(sample-strength x-values %))
         (reduce +))))
```

In part two we're told that the values of the `X` register represent the
horizontal position of the center of a three pixel wide sprite on a small
CRT screen. The electron bean sweeps the screen left to right and at each
clock cycle it can turn on a single pixel. If at any clock cycle the beam
overlaps with the sprite then we turn on the pixel under the electron
beam. The CRT is made of 6 lines of 40 pixels each, and our program is
supposed to paint a string of uppercase characters.

We turn a single pixel on with

```clojure

(defn turn-on
  [x-values clock crt]
  (let [beam-pos (mod clock 40)
        sprite-pos (nth x-values clock)]
    (if (<= (dec beam-pos) sprite-pos (inc beam-pos))
      (update crt clock (fn [_] "#"))
      crt)))
```

and we paint the whole screen with

```clojure
(defn paint
  [x-values crt]
  (reduce (fn [crt clock]
            (turn-on x-values clock crt))
          crt
          (range (* 6 40))))
```

So that the solution to part two is just

```clojure
(defn part-2
  [input]
  (let [opcodes (parse-input input)
        x-values (collect-x-values opcodes)
        crt (vec (repeat (* 6 40) "."))]
    (->> crt
         (paint x-values)
         (partition 40)
         (mapv #(reduce str %))
         (mapv println))))
```

Note that our CRT is a single 240 value vector (as opposed to a vector
of vectors) and it's broken into single lines only when printing the
result.

Day 11 - Monkey in the Middle
-----------------------------

[Solution][d11-clj] - [Back to top][top]

In day 11 we're watching some monkeys throw stuff around. We're given the
initial state (which monkey has what and what will it do with it) and are
asked to find out how many times the two most active monkeys will look at
one of the items. As usual we start parsing the input: each monkey ends at
a double `\n`, and for each one we'll need to figure out a list of numbers
(the _items_), a function that will calculate a new number for each _item_
and a test that will decide to what monkey the _item_ will be thrown after
a new value is calculated.

```clojure
(defn parse-monkey
  [lines]
  (let [[_ items op & destination] 
        (str/split-lines lines)]
    {:items (mapv parse-long (re-seq #"\d+" items))
     :update (parse-update op)
     :destination (parse-destination destination)
     :inspections 0}))
```

The update calculation seems to only involve addition and multiplication,
with each operand either a number or the old value. Our parsing function
will return a function of the current _item_ value that will replace the
`"old"` string with that value and perform the calculation in the input.

```clojure
(defn parse-update
  [line]
  (let [[a op b] (drop 4 (str/split line #"\s+"))
        op-fn (condp = op
                "+" +
                "*" *)]
    (fn [x]
      (letfn [(eval [arg] (if (= "old" arg) x (parse-long arg)))]
        (apply op-fn (map eval [a b]))))))
```

The function for deciding which monkey each item should be thrown to
is always a test to check if an _item_ value is divisible by a certain
number, with the number on the first line, and the monkeys that should
receive the new _item_ on the second and third lines

```clojure
(defn parse-destination
  [lines]
  (let [[modulo on-true on-false]
        (->> lines (map #(re-find #"\d+" %)) (map parse-long))]
    (fn [x] (if (zero? (rem x modulo)) on-true on-false))))
```

Now that we have the input parsed we need code for playing a round of the
game, where each monkeys takes its turn to look at the items, updating
them and throwing them to another monkey. For the `i`th monkey's turn we
do loop over the monkey's items, update the values, decide where the new
value will go and update the monkey list accordingly. Note that the
problem says that after updating a value and before deciding where it goes
we should divide the new value by `3`, rounding down.

```clojure
(defn take-turn
  [monkeys i] 
  (loop [monkeys monkeys]
    (let [monkey (monkeys i)
          item (first (:items monkey))]
      (if item
        (let [new-item ((:update monkey) item)
              de-stressed (quot new-item 3)
              destination ((:destination monkey) de-stressed)]
          (recur (-> monkeys
                     (update-in [i :items] subvec 1)
                     (update-in [i :inspections] inc)
                     (update-in [destination :items] conj de-stressed))))
        monkeys))))
```

For playng a complete round (where each monkey takes its turn) we use

```clojure
(defn play-round
  [monkeys]
  (reduce take-turn monkeys (range (count monkeys))))
```

and we can put it all together to solve part one.

```clojure
(defn part-1
  [filename]
  (->> filename
       slurp
       parse-input
       (iterate play-round)
       (drop 20)
       first
       (map :inspections)
       (sort >)
       (take 2)
       (apply *)))
```

In part two we no longer divide values by three after inspection, and we
are doing 10'000 rounds instead if 20. A quick check gives an overflow
error, so some trick is required to keep numbers small. Note that all
the update operations are either a sum or a product, and all divisibility
checks are done on prime numbers. That has to mean something... aaaand
a quick duckduckgo search later says [modular arithmetic][wiki-mod] is
the key. Under modulo arithmetic

- if `a ≡ b (mod n)` then `(a + c) ≡ (b + c) (mod n)`
- if `a ≡ b (mod n)` then `(a * c) ≡ (b * c) (mod n)`
- if `a ≡ b (mod n)` then `(a * c) ≡ (b * c) (mod c * n)`

or written in clojure

- if `(= (rem a n) (rem b n))` then `(= (rem (+ a c) n) (rem (+ b c) n)`
- if `(= (rem a n) (rem b n))` then `(= (rem (* a c) n) (rem (* b c) n)`
- if `(= (rem a n) (rem b n))` then `(= (rem (* a c) (* c n) (rem (* b c) (* c n)`

Since we're only doing additions and multiplications that means that if
instead of keeping the result of each update we keep just the remainder
of the division by a large enough number we're going to be fine, since
the divisibility check will have the same result. What should that large
enough number be? For the first monkey we're checking that the result of
the update is divisible by `23` so we could just keep `(mod n 23)`. For
the second one we're checking agains `19`, so if we want `n` to be
divisible by both `23` and `19` we should keep `(mod n (* 23 19))` and
so on. We can find the number we need with

```clojure
(defn calc-big-num
  [input]
  (->> input
       (re-seq #"by (\d+)")
       (map #(parse-long (second %)))
       (apply *)))

```

and since for part two we're no longer dividing the updated valyes by
three we should factor that out

```clojure
(defn stress-reducer
  [monkey]
  (update monkey :update (partial comp #(quot % 3))))
```

This one is fun: afer parsing each monkey is a map, and its `:update`
key holds the function used to re-calc _item_ values. In part one we
need to divide each value by three after calculation: this one, called
after parsing will update that function and chain it with the division
we need. With that in place we need to update our `parse-monkey`
function to take an extra argument and return a different `:update`
function

```clojure
(defn parse-monkey
  [big-num lines]
  (let [[_ items op & destination]
        (str/split-lines lines)]
    {:items (mapv parse-long (re-seq #"\d+" items))
     :update (comp #(mod % big-num) (parse-update op))
     :destination (parse-destination destination)
     :inspections 0}))

```

Also our `take-turn` function no longer neds to divice _item_ values by
three

```clojure
(defn take-turn
  [monkeys i]
  (loop [monkeys monkeys]
    (let [monkey (monkeys i)
          item (first (:items monkey))]
      (if item
        (let [new-item ((:update monkey) item)
              destination ((:destination monkey) new-item)]
          (recur (-> monkeys
                     (update-in [i :items] subvec 1)
                     (update-in [i :inspections] inc)
                     (update-in [destination :items] conj new-item))))
        monkeys))))
```

and `part-1` needs to `(mapv stress-reducer)` over the monkeys after
parsing and before iterating `play-round`.

`part-2` does not need that, it just needs a different number of rounds
to play

```clojure
(defn part-2
  [filename]
  (->> filename
       slurp
       parse-input
       (iterate play-round)
       (drop 10000)
       first
       (map :inspections)
       (sort >)
       (take 2)
       (apply *)))
```

Day 12 - Hill Climbing Algorithm
--------------------------------

[Solution][d12-clj] - [Back to top][top]

In day 12 we're climbing a hill. Our input shows a grid of heights, with
`a` being the lowest and `z` the highest. Two positions in the grid, marked
`S` and `E` respectively, indicate where we start and where we want to go.
Let'start reading the grid into a vector of vectors. We don't care about
the values in the grid, as long as they mantain the right order (`a` then
`b` then `c`...) so we can just map each character to it's `int` value.

```clojure
(defn read-grid
  [data]
  (->> data
       str/split-lines
       (mapv #(mapv int %))))
```

Next we want to find where our starting and ending positions are in the
grid. This works enumerating each possible pair of coordinates in the grid,
checking if the corresponding value is the `int` for `S` or `E` (83 and 69
respectively) and returning the non `nil` values into a map with keys
`:start` and `:goal`.

```clojure
(defn find-positions
  [grid]
  (let [coords 
        (for [r (range (count grid))
              c (range (count (first grid)))]
          [r c])]
    (->> coords
         (map #(case (get-in grid %)
                 83 {:start %}
                 69 {:goal %}
                 nil))
         (filter identity)
         (into {}))))
```

Since we're told that the start position is at height `a` and the end
position is at height `z` we need to replace their values in the grid we
parsed.

```clojure
(defn replace-position-values
  [grid {:keys [start goal]}]
  (-> grid
      (assoc-in start (int \a))
      (assoc-in goal (int \z))))
```

Putting all that together we can now parse the input. This will return
a map with all we need to know to solve the problem: a `:grid` with the
height values, a `:start` position and a `:goal` position.

``` clojure
(defn parse-input
  [filename]
  (let [grid (read-grid filename)
        positions (find-positions grid)]
    (into {:grid (replace-position-values grid positions)}
          positions)))
```

We're asked to find the path from `S` to `E`, moving one step at a time
and only to positions that are at most 1 level above the one we are moving
from. It's time to learn search algotihms, but I'm a cheat so:

- we'll do [BFS][wiki-bfs]
- we'll do it backwards since in part two we'll need to search the
  shortest of the paths starting at height `a`. Doing it backwards
  saves work since we only need to search once: all steps have the
  same weight and BFS assures us that the first time we visit a
  certain grid position we got there by the shortest path.
- doing it backwards means that we're no longer moving to heights
  at most one level above, but to eights at most one level down

First we need a way to get the neighbours of a diven grid position

```clojure
(defn get-neighbours 
  [grid [x y :as pos]]
  (let [min-h (dec (get-in grid pos))]
    (->> [[(dec x) y]
          [(inc x) y]
          [x (dec y)]
          [x (inc y)]] 
         (filter #(if-let [new-h (get-in grid %)]
                    (<= min-h new-h))))))
```

then we neead a function that given our parsed input and a position
tell's us to stop searching if we reached the goal

```clojure
(defn goal-reached-part-1?
  [{:keys [start]} pos]
  (= pos start))
```

with all that our search function is

```clojure
(defn bfs-search
  [goal-fn {:keys [grid goal] :as world}]
  (loop [queue [{:d 0 :pos goal}] visited #{}]
    (if-not (empty? queue)
      (let [[{:keys [d pos] :as cur} & rest] queue]
        (cond
          (goal-fn world pos)
          d

          (visited pos)
          (recur (vec rest) (conj visited pos))

          :else
          (recur (->> (get-neighbours grid pos)
                      (filter #(not (visited %)))
                      (map (fn [p] {:d (inc d) :pos p}))
                      (into (vec rest)))
                 (conj visited pos))))
      nil)))
```

Part one then is just

```clojure
(defn part-1
  [filename]
  (->> filename
       slurp
       parse-input
       (bfs-search goal-reached-part-1?)))
```

And part two just needs a new goal function

```clojure
(defn goal-reached-part-2?
  [{grid :grid} pos]
  (= (get-in grid pos) (int \a)))

(defn part-2
  [filename]
  (->> filename
       slurp
       parse-input
       (bfs-search goal-reached-part-2?)))
```

Day 13 - Distress Signal
------------------------

[Solution][d13-clj] - [Back to top][top]

In day 3 we're comparing list of numbers:

- numbers are compared the usual way
- lists are compared member by member
- an empty list is always smaller than a non-empty list
- when comparing a number and a list we transform the number into a
  single element list and compare the two lists

As usual we start parsing the input. Since the input looks like valid
clojure code we'll cheat and parse the input lists as vectors using
`read-string`. That `(filter seq)` call is the idiomatic way of filtering
out empty strings.

```clojure
(defn parse-input
  [filename]
  (->> filename
       slurp
       str/split-lines
       (filter seq)
       (map read-string)))
```

We then need a function to compare pairs of the vectors we just read. Like
compare functions everywhere we're returning `-1`, `0` or `1` if the left
side is less than, equal to or greather-than the right side.

```clojure
(defn packet-compare
  [left right]
  (cond
    (and (int? left) (int? right))     (compare left right)
    (int? left)                        (recur [left] right)
    (int? right)                       (recur left [right])
    (and (empty? left) (empty? right))  0
    (empty? left)                      -1
    (empty? right)                      1
    :else (loop [[l & ls] left
                 [r & rs] right]
            (let [cmp (packet-compare l r)]
              (if (and (zero? cmp) (or ls rs))
                (recur ls rs)
                cmp)))))
```

We're now ready to solve part one, which asks which of the pairs is in
the correct order, that is for which pairs of lists the firt one (the one
"on the left") is smaller than the second one ("on the right"). We just
partition the input in pairs, apply the compare function above to each
pair and save the results into an indexed vector, saving the indexes
of the pairs in the correct order (and taking care to fix the indexes:
our vecor is 0-based, the problem asks for 1-based). For part one we
want the sum of the indexes, so

```clojure
(defn is-in-the-right-order?
  [[ _ compare-result]]
  (<= compare-result 0))

(defn part-1
  [filename]
  (->> filename
       parse-input
       (partition 2)
       (map #(apply packet-compare %))
       (map-indexed vector)
       (filter is-in-the-right-order?)
       (map first)
       (map inc)
       (apply +)))
```

In part two we are told to add two special lists to the ones we parsed,
sort the result with the above compare function and find the indexes at
which the lists we added end after sorting. Easy.

```clojure
(defn is-delimiter?
  [[_ packet]]
   (or (= [[2]] packet) (= [[6]] packet)))

(defn part-2
  [filename]
  (->> filename
       parse-input
       (cons [[2]])
       (cons [[6]])
       (sort packet-compare)
       (map-indexed vector)
       (filter is-delimiter?)
       (map first)
       (map inc)
       (apply *)))
```

Day 14 - Regolith Reservoir
---------------------------

[Solution][d14-clj] - [Back to top][top]

In day 14 we're tracking gfains of sand falling down a cave. Each line in the input contains one or more pairs of coordinates separated by `->`
and representing the segments (horizontal or vertical) that make up some
rock shelves in the cave. Each grain of sand falls dowsn from position
`[500 0]` (y grows toward the bottom). At each step sand will fall down
at most one unit: if the new position is not empty then it will move one
unit to the left and if even that position is occupied it will move one
unit to the right. If neither of the three possible positions is empty
the grain of sand will stop at the current position and another one will
start falling.

For part one we're told that after enough sand has fallen in the cave
every new grain of sand we'll fall to the bottom left and keep falling infinitely. We're asked how many grains of sand will fall before that
happens.

As always we start parsing the input: we want the numbers on each line,
which we'll collect in `[x y]` pairs and then in `[[x0 y0] [x1 y1]]`
pairs representing segments

```clojure
(defn parse-lines
  [data]
  (->> data
       str/split-lines
       (map #(re-seq #"\d+" %))
       (map #(map parse-long %))))

(defn parse-segments
  [numbers]
  (let [pairs (partition 2 numbers)]
    (map vector pairs (drop 1 pairs))))
```

We'll also need to find the cave bottom (i.e. the y coordinate of the
bottom rock shelf)

```clojure
(defn find-cave-bottom
  [lines]
  (->> lines
       (map #(take-nth 2 (drop 1 %)))
       (flatten)
       (reduce max)))
```

We'll now add each pair that makes up a rock shelf to a `set` and join
all those sets to get the complete cave. Looking at the input it seems
like there's no guarantee that the segment bounds will be in the correct
left-to-right or top-to-bottom order so well need a utility function to
take care of that, as well as the fact that clojure's [ranges][docs-range]
don't include the end values.

```clojure
(defn irange
  [a b]
  (range (min a b) (inc (max a b))))

(defn add-rocks
  [rocks [[x0 y0] [x1 y1]]]
  (into rocks (for [x (irange x0 x1)
                    y (irange y0 y1)]
                [x y])))

(defn parse-rock-shelves
  [number-lines]
  (->> number-lines
       (map parse-segments)
       (map #(reduce add-rocks #{} %))
       (reduce set/union)))
```

Parsing input is then

```clojure
(defn parse-input
  [data]
  (let [number-lines (parse-lines data)
        cave-bottom (find-cave-bottom number-lines)
        rocks (parse-rock-shelves number-lines)]
    {:rocks rocks :sand #{} :cave-bottom cave-bottom}))
```

Just to check that everything is good let's print the resulting cave.
We need a function that given a pair `[x y]` tell's us what's in the
cave at that position

```clojure
(defn get-in-cave
  [{:keys [sand rocks cave-bottom]} [x y]]
  (let [rock-floor (+ 2 cave-bottom)]
    (cond (sand [x y])     \o
          (rocks [x y])    \#
          :else            \.)))
```

and a function to iterat from the top left to the bottom right of the
cave printing what it finds at each pair of coordinates. We'll cheat and
hardcode the boundaries (note that the x and y loops are swapped since
we want to draw all the `x` positions for a given `y` before moving to
the level below)

```clojure
(defn print-cave
  [cave]
  (->> (for [y (range 0 10)
             x (range 494 504)]
         [x y])
       (map #(get-in-cave cave %))
       (partition 10)
       (map #(apply str %))))
```

On our thest input the cave looks like we expect,

```text
(".........."
 ".........."
 ".........."
 ".........."
 "....#...##"
 "....#...#."
 "..###...#."
 "........#."
 "........#."
 "#########.")
 ```

To solve part one we want to drop a gain of sand at a time and stop
as soon as every grain of sand passes the bottom rock shelf and falls
forever. There are probably smart ways to do it but simulating each
grain of sand should work. To do that we need a couple of functions;
the first one checks if the cave is 'empty' at a given position

```clojure
(defn position-empty?
  [cave [x y]]
  (condp = (get-in-cave cave [x y])
    \# false
    \o false
    true))
```

and the other decides where a grain of sand will go next

```clojure
(defn next-position
  [cave [x y]]
  (->> [[x (inc y)]
        [(dec x) (inc y)]
        [(inc x) (inc y)]]
       (filter #(position-empty? cave %))
       first))
```

Now we need only to decide when to stop

```clojure
(defn falls-to-infinite
  [cave [_ y]]
  (> y (:cave-bottom cave)))
```

and we're ready to simulate the grains of sand motion: we follow a grain
of sand that pops into existence at position `[500 0]` until it settles
down and repeat until the above stop function returns true.

```clojure
(defn drop-sand-until
  [cave stop-fn]
  (loop [cave cave
         grain-of-sand [500 0]]
    (if-not (stop-fn cave grain-of-sand)
      (if-let [[x y] (next-position cave grain-of-sand)]
        (recur cave [x y])
        (update cave :sand conj grain-of-sand))
      (assoc cave :settled true))))
```

For part one we want to know how many grains of sand will settle down
before the next one falls to infinity

```clojure
(defn part-1
  [data]
  (let [cave (parse-input data)]
    (->> cave
         (iterate #(drop-sand-until % falls-to-infinite))
         (drop-while #(not (:settled %)))
         first
         :sand
         count)))
```

For part two we are told that two levels below the bottom rock shelf
there's a floor that extends infinitely on both sides and sand will
continue pouring into the cave just until the position at `[500 0]`
is occupied by the sand piling up. We can reuse almost all of the code
for part one, we just need to update the `get-in-cave` function to
check for the cave's floor and write a new function telling us when
to stop

```clojure
(defn get-in-cave
  [{:keys [sand rocks cave-bottom]} [x y]]
  (let [rock-floor (+ 2 cave-bottom)]
    (cond (sand [x y])     \o
          (rocks [x y])    \#
          (= y rock-floor) \#
          :else            \.)))
          
(defn sand-fills-cave
  [cave _]
  ((:sand cave) [500 0]))
```

And part two is just

```clojure
(defn part-2
  [data]
  (let [cave (parse-input data)]
    (->> cave
         (iterate #(drop-sand-until % sand-fills-cave))
         (drop-while #(not (:settled %)))
         first
         :sand
         count)))
```

Day 15 - Beacon Exclusion Zone
------------------------------

[Solution][d15-clj] - [Back to top][top]

In day 15 we're searching for a beacon on a square area. The input gives
us a list of sensors, each one of which knows it's own position and the
position of the nearest beacon. Distances are calculated with the
[Mahnattan's Distance][wiki-md].

As usual we start parsing the input: for each sensor we want the position,
the position of the nearest beacon ant it's distance (it will be useful
later).

```clojure
(defn dist
  [[a b] [c d]]
  (+ (abs (- a c)) (abs (- b d))))

(defn parse-line
  [line]
  (let [[posn nearest] 
        (->> line
             (re-seq #"-?\d+")
             (map parse-long)
             (partition 2))]
    {:posn posn
     :nearest nearest
     :range (dist posn nearest)}))

(defn parse-input
  [data]
  (->> data
       str/split-lines
       (map parse-line)))
```

Each sensor knows about its nearest beacon, so each sensor defines a
diamond-shaped area that can't contain other beacons, the _radius_ of the
area being the distance to the nearest beacon. For part one we want to
know how many grid positions at a given `y` coord **can't** be occupied by
a beacon. We do that by joining the slices of the sensor diamonds at
a fixed `y` position (note that they may overlap), counting how many grid
cells the joined slices cover and subtracting the number of actual
beacons at the given `y` coordinate. Given a sensor `S` at grid (`Sx`,
`Sy`) and its closest beacon `B` at distance `R` below

```text
.....................
.....................
..........t.......... t is (Sx, Sy - R)
.........###.........
........#####........
.......#######.......
......#########......
.....###########.....
....#############....
...###############...
..#################..
.l########S########r. l is (Sx - R, Sy), r is (Sx + R, Sy)
..#################..
...###############...
....B############....
.....###########.....
......#########......
.......#######.......
........#####........
.........###.........
..........b.......... b is (Sx, Sy + R)
.....................
.....................
```

the _slice_ at any given y is easy to find

- if `y` is less than `Sy - R` or greather than `Sy + R` there's no slice
- if `y` is between `Sy - R` and `Sy + R` then calling `dy` the absolute
  value of `Sy - y`, the slice goes from `Sx - R + dy` to `Sx + R - dy`
  because of how the Manhattan distance works.

We can start defining a function that given a sensor and a `y` position
calculates the slice of diamond on the `y` coordinate for that sensor,
if any

```clojure
(defn exclude-at-y
  [{:keys [posn range]} y]
  (let [[sx sy] posn
        dx (- range (abs (- y sy)))]
    (when (>= dx 0)
      [(- sx dx) (+ sx dx)])))
```

and applying it to every sensor

```clojure
(defn exclusions-at-y
  [sensors y]
  (->> sensors
       (map #(exclude-at-y % y))
       (filter identity)
       (sort-by first)))
```

we get a list of slices sorted left to right. We can then merge the slices
with

```clojure
(defn merge-ranges
  [merged [c d :as r]]
  (if-let [[a b] (first merged)]
    (if (<= c b)
      (conj (drop 1 merged) [(min a c) (max b d)])
      (conj merged r))
    (conj merged r)))
```

and count the grid cells covered with

```clojure
(defn count-range
  [[a b]]
  (+ (- b a) 1))

(defn count-covered
  [ranges]
  (->> ranges
       (reduce merge-ranges [])
       (map count-range)
       (apply +)))
```

To count the beacons at a given `y` positions add all the beacons to a
set (multiple sensors can have the same nearest beacon and the set will
take care of removing duplicates), filter by `y` position and count

```clojure
(defn count-beacons-at-y
  [sensors y]
  (->> sensors
       (map :nearest)
       (into #{})
       (filter #(= (second %) y))
       count))
```

With all that in place part 1 is solved with

```clojure
(defn part-1
  [sensors y]
  (let [ranges (exclusions-at-y sensors y)
        covered (count-covered ranges)
        beacons (count-beacons-at-y sensors y)]
    (- covered beacons)))

(part-1 (parse-input (slurp "../inputs/day_15_test.txt")) 10)
(part-1 (parse-input (slurp "../inputs/day_15.txt")) 2000000)
```


---

Notes
-----

<sup>†</sup> many ideas for Day 11 were blatantly taken from [pbruyninckx][d11-pbruyninckx]'s code

<sup>‡</sup> even more than Day 11 code for Day 13 is shamelessy copied
from [pbruyninckx][d13-pbruyninckx]


[top]: #advent-of-code-2022

[d01]: #day-1---calorie-counting
[d02]: #day-2---rock-paper-scissors
[d03]: #day-3---rucksack-reorganization
[d04]: #day-4---camp-cleanup
[d05]: #day-5---supply-stacks
[d06]: #day-6---tuning-trouble
[d07]: #day-7---no-space-left-on-device
[d08]: #day-8---treetop-tree-house
[d09]: #day-9---rope-bridge
[d10]: #day-10---cathode-ray-tube
[d11]: #day-11---monkey-in-the-middle
[d12]: #day-12---hill-climbing-algorithm
[d13]: #day-13---distress-signal
[d14]: #day-14---regolith-reservoir
[d15]: #day-15---beacon-exclusion-zone
[notes]: #notes


[d01-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_01.clj
[d02-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_02.clj
[d03-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_03.clj
[d04-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_04.clj
[d05-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_05.clj
[d06-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_06.clj
[d07-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_07.clj
[d08-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_08.clj
[d09-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_09.clj
[d10-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_10.clj
[d11-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_11.clj
[d12-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_12.clj
[d13-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_13.clj
[d14-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_14.clj
[d15-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_15.clj


[docs-slurp]: https://clojuredocs.org/clojure.core/slurp
[docs-apply]: https://clojuredocs.org/clojure.core/apply
[docs-seq]: https://clojuredocs.org/clojure.core/seq
[docs-set]: https://clojuredocs.org/clojure.core/set
[docs-intersection]: https://clojuredocs.org/clojure.set/intersection
[docs-range]: https://clojuredocs.org/clojure.core/range
[d11-pbruyninckx]: https://github.com/pbruyninckx/aoc2022/blob/main/src/aoc/day11.clj
[wiki-mod]: https://en.wikipedia.org/wiki/Modular_arithmetic
[wiki-bfs]: https://en.wikipedia.org/wiki/Breadth-first_search
[d13-pbruyninckx]: https://github.com/pbruyninckx/aoc2022/blob/main/src/aoc/day13.clj
[wiki-md]: https://en.wikipedia.org/wiki/Taxicab_geometry
