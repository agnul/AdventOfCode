(ns day_10
  (:require [clojure.string :as str]))

(defn parse-opcode
  [line]
  (let [[op arg] (str/split line #"\s+")]
    (if-not (= op "noop") (parse-long arg) 0)))

(defn parse-input
  [input]
  (->> input
       str/split-lines
       (mapv parse-opcode)))

(defn collect-x-values
  [opcodes]
  (reduce
   (fn [x-values op-arg]
     (let [prev (peek x-values)]
       (if-not (zero? op-arg)
         (conj (conj x-values prev) (+ prev op-arg))
         (conj x-values prev))))
   [1] opcodes))

(defn sample-strength
  [x-values clock]
  (* clock (nth x-values (dec clock))))

(defn turn-on
  [x-values clock crt]
  (let [beam-pos (mod clock 40)
        sprite-pos (nth x-values clock)]
    (if (<= (dec beam-pos) sprite-pos (inc beam-pos))
      (update crt clock (fn [_] "#"))
      crt)))

(defn paint
  [x-values crt]
  (reduce (fn [crt clock]
            (turn-on x-values clock crt))
          crt
          (range (* 6 40))))

(defn part-1
  [input]
  (let [opcodes (parse-input input)
        x-values (collect-x-values opcodes)
        max-clock (count x-values)
        sample-times (range 20 max-clock 40)]
    (->> sample-times
         (map #(sample-strength x-values %))
         (reduce +))))

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

(part-1 (slurp "../inputs/day_10_test.txt"))
(part-1 (slurp "../inputs/day_10.txt"))

(part-2 (slurp "../inputs/day_10_test.txt"))
(part-2 (slurp "../inputs/day_10.txt"))
