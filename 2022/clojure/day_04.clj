(ns day_04
  (:require [clojure.string :as str]))

(defn read_input
  [filename]
  (partition 4 (map parse-long (str/split (slurp filename) #"[\n,-]"))))

(defn fully_contained?
  [a b c d]
  (or (<= a c d b) (<= c a b d)))

(defn overlapping?
  [a b c d]
  (or (fully_contained? a b c d)
      (<= a c b d)
      (<= c a d b)))

(defn part-1
  [filename]
  (->> (read_input filename)
       (filter #(apply fully_contained? %))
       (count)))

(defn part-2
  [filename]
  (->> (read_input filename)
       (filter #(apply overlapping? %))
       (count)))

(part-1 "../inputs/day_04_test.txt")
(part-1 "../inputs/day_04.txt")

(part-2 "../inputs/day_04_test.txt")
(part-2 "../inputs/day_04.txt")
