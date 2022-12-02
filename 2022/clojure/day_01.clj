(ns day_01
  (:require [clojure.string :as str]))

(defn parse-meal
  [lines]
  (mapv #(Long/parseLong %) (str/split lines #"\n")))

(defn parse-input
  [filename]
  (mapv parse-meal (str/split (slurp filename) #"\n\n")))

(defn part-1
  [filename]
  (let [meals (parse-input filename)]
    (apply max (mapv #(reduce + %) meals))))

(defn part-2
  [filename]
  (let [meals (parse-input filename)
        calories (mapv #(reduce + %) meals)]
    (reduce + (take 3 (sort > calories)))))

(part-1 "../inputs/test_day_01.txt")
(part-1 "../inputs/day_01.txt")

(part-2 "../inputs/test_day_01.txt")
(part-2 "../inputs/day_01.txt")
