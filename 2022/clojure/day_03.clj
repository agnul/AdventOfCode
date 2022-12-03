(ns day_03
  (:require [clojure.string :as str]
            [clojure.set :as set]))

(defn read_input
  [filename]
  (map seq (str/split (slurp filename) #"\n")))

(defn find-misplaced-item
  [rucksack]
  (let [half (/ (count rucksack) 2)
        first-half (set (take half rucksack))
        second-half (set (drop half rucksack))]
  (first (set/intersection first-half second-half))))

(defn is_upper?
  [letter]
  (<= (int \A) (int letter) (int \Z)))

(defn score
  [letter]
  (cond
    (is_upper? letter) (+ 27 (- (int letter) (int \A)))
    :else              (+  1 (- (int letter) (int \a)))))

(defn find-badge
  [group]
  (map first (map #(apply set/intersection %) group)))

(defn part-1
  [filename]
  (let [rucksacks (read_input filename)]
    (->> rucksacks
         (map find-misplaced-item)
         (map score)
         (reduce +))))

(defn part-2
  [filename]
  (let [elf-groups (partition 3 (map set (read_input filename)))]
    (->> elf-groups
         (find-badge)
         (map score)
         (reduce +))))

(part-1 "../inputs/day_03_test.txt")
(part-1 "../inputs/day_03.txt")

(part-2 "../inputs/day_03_test.txt")
(part-2 "../inputs/day_03.txt")
