(ns day_04
  (:require [clojure.string :as str]
            [clojure.set :as set]))

(defn read_assignment
  [line]
  (let [[a b c d] (map parse-long (str/split line #"-|,"))]
    (list
     (set (range a (+ 1 b)))
     (set (range c (+ 1 d))))))

(defn read_input
  [filename]
  (map read_assignment (str/split (slurp filename) #"\n")))

(defn fully-contained?
  [assignment]
  (let [[first second] assignment]
    (or (set/subset? first second)
        (set/subset? second first))))

(defn overlapping?
  [assignment]
  (let [[first second] assignment]
    (> (count (set/intersection first second)) 0)))

(defn part-1
  [filename]
  (->> (read_input filename)
       (filter fully-contained?)
       (count)))

(defn part-2
  [filename]
  (->> (read_input filename)
       (filter overlapping?)
       (count)))

(part-1 "../inputs/day_04_test.txt")
(part-1 "../inputs/day_04.txt")

(part-2 "../inputs/day_04_test.txt")
(part-2 "../inputs/day_04.txt")
