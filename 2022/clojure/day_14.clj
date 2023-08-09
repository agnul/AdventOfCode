(ns day_14
  (:require [clojure.set :as set]
            [clojure.string :as str]))

(defn parse-lines
  [data]
  (->> data
       str/split-lines
       (map #(re-seq #"\d+" %))
       (map #(map parse-long %))))

(defn find-cave-bottom
  [lines]
  (->> lines
       (map #(take-nth 2 (drop 1 %)))
       (flatten)
       (reduce max)))

(defn parse-segments
  [numbers]
  (let [pairs (partition 2 numbers)]
    (map vector pairs (drop 1 pairs))))

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

(defn parse-input
  [data]
  (let [number-lines (parse-lines data)
        cave-bottom (find-cave-bottom number-lines)
        rocks (parse-rock-shelves number-lines)]
    {:rocks rocks :sand #{} :cave-bottom cave-bottom}))

(defn get-in-cave
  [{:keys [sand rocks cave-bottom]} [x y]]
  (let [rock-floor (+ 2 cave-bottom)]
    (cond (sand [x y])     \o
          (rocks [x y])    \#
          (= y rock-floor) \#
          :else            \.)))

(defn print-cave
  [cave]
  (->> (for [y (range 0 10)
             x (range 494 504)]
         [x y])
       (map #(get-in-cave cave %))
       (partition 10)
       (map #(apply str %))))

(defn position-empty?
  [cave [x y]]
  (condp = (get-in-cave cave [x y])
    \# false
    \o false
    true))

(defn next-position
  [cave [x y]]
  (->> [[x (inc y)]
        [(dec x) (inc y)]
        [(inc x) (inc y)]]
       (filter #(position-empty? cave %))
       first))

(defn falls-to-infinite
  [cave [_ y]]
  (> y (:cave-bottom cave)))

(defn sand-fills-cave
  [cave _]
  ((:sand cave) [500 0]))

(defn drop-sand-until
  [cave stop-fn]
  (loop [cave cave
         grain-of-sand [500 0]]
    (if-not (stop-fn cave grain-of-sand)
      (if-let [[x y] (next-position cave grain-of-sand)]
        (recur cave [x y])
        (update cave :sand conj grain-of-sand))
      (assoc cave :settled true))))

(defn part-1
  [data]
  (let [cave (parse-input data)]
    (->> cave
         (iterate #(drop-sand-until % falls-to-infinite))
         (drop-while #(not (:settled %)))
         first
         :sand
         count)))

(defn part-2
  [data]
  (let [cave (parse-input data)]
    (->> cave
         (iterate #(drop-sand-until % sand-fills-cave))
         (drop-while #(not (:settled %)))
         first
         :sand
         count)))

(def test-input "498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
")

(print-cave (parse-input test-input))

(part-1 test-input)
(part-1 (slurp "../inputs/day_14.txt"))

(part-2 test-input)
(part-2 (slurp "../inputs/day_14.txt"))


