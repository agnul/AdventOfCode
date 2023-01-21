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



--- 
[top]: #advent-of-code-2022

[d01]: #day-1---calorie-couting
[d02]: #day-2---rock-paper-scissors
[d03]: #day-3---rucksack-reorganization
[d04]: #day-4---camp-cleanup


[d01-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_01.clj
[d02-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_02.clj
[d03-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_03.clj
[d04-clj]: https://github.com/agnul/AdventOfCode/blob/main/2022/clojure/day_04.clj


[docs-slurp]: https://clojuredocs.org/clojure.core/slurp
[docs-apply]: https://clojuredocs.org/clojure.core/apply
[docs-seq]: https://clojuredocs.org/clojure.core/seq
[docs-set]: https://clojuredocs.org/clojure.core/set
[docs-intersection]: https://clojuredocs.org/clojure.set/intersection