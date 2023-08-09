(ns day_15 
  (:require [clojure.string :as str]))

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

(defn exclude-at-y
  [{:keys [posn range]} y]
  (let [[sx sy] posn
        dx (- range (abs (- y sy)))]
    (when (>= dx 0)
      [(- sx dx) (+ sx dx)])))

(defn exclusions-at-y
  [sensors y]
  (->> sensors
       (map #(exclude-at-y % y))
       (filter identity)
       (sort-by first)))

(defn merge-ranges
  [merged [c d :as r]]
  (if-let [[a b] (first merged)]
    (if (<= c b)
      (conj (drop 1 merged) [(min a c) (max b d)])
      (conj merged r))
    (conj merged r)))

(defn count-range
  [[a b]]
  (+ (- b a) 1))

(defn count-covered
  [ranges]
  (->> ranges
       (reduce merge-ranges [])
       (map count-range)
       (apply +)))

(defn count-beacons-at-y
  [sensors y]
  (->> sensors
       (map :nearest)
       (into #{})
       (filter #(= (second %) y))
       count))

(defn part-1
  [sensors y]
  (let [ranges (exclusions-at-y sensors y)
        covered (count-covered ranges)
        beacons (count-beacons-at-y sensors y)]
    (- covered beacons)))

(count-beacons-at-y (parse-input (slurp "../inputs/day_15_test.txt")) 10)

(part-1 (parse-input (slurp "../inputs/day_15_test.txt")) 10)
(part-1 (parse-input (slurp "../inputs/day_15.txt")) 2000000)
