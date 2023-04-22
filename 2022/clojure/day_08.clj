(ns day_08
  (:require [clojure.string :as str]))

(defn parse-input
  [string]
  (let [lines (str/split-lines string)
        rows (mapv #(mapv parse-long (str/split % #"")) lines)
        columns (apply mapv vector rows)
        size (count (first rows))]
    {:rows rows :columns columns :size size}))

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

(defn part-1
  [filename]
  (let [data (->> filename slurp parse-input)
        size (:size data)]
    (count (filter true?
                   (for [r (range size)
                         c (range size)]
                     (visible? data r c))))))

(defn part-2
  [filename]
  (let [data (->> filename slurp parse-input)
        size (:size data)]
    (apply max (for [r (range size)
                     c (range size)]
                 (score data r c)))))

(part-1 "../inputs/day_08_test.txt")
(part-1 "../inputs/day_08.txt")

(part-2 "../inputs/day_08_test.txt")
(part-2 "../inputs/day_08.txt")
