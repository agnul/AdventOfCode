(ns day_13
  (:require [clojure.string :as str]))

(defn parse-input
  [filename]
  (->> filename
       slurp
       str/split-lines
       (filter seq)
       (map read-string)))

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

(defn is-in-the-right-order?
  [[ _ compare-result]]
  (<= compare-result 0))

(defn is-delimiter?
  [[_ packet]]
   (or (= [[2]] packet) (= [[6]] packet)))

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

(part-1 "../inputs/day_13_test.txt")
(part-2 "../inputs/day_13_test.txt")

(part-1 "../inputs/day_13.txt")
(part-2 "../inputs/day_13.txt")
