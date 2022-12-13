(ns day_09
  (:require [clojure.string :as str]))

(defn parse-move
  [string]
  (let [[direction cnt] (str/split string #"\s")]
    (list (keyword direction) (parse-long cnt))))

(defn parse-input
  [filename]
  (->> filename
       slurp
       str/split-lines
       (map parse-move)))

(def test-input
  (->> "R 4\nU 4\nL 3\nD 1\nR 4\nD 1\nL 5\nR 2"
       str/split-lines
       (map parse-move)))

(defn add
  [[x0 y0] [x1 y1]]
  [(+ x0 x1) (+ y0 y1)])

(defn sub
  [[x0 y0] [x1 y1]]
  [(- x0 x1) (- y0 y1)])

(defn delta
  [n1 n2]
  (let [[dx dy] (sub n1 n2)]
    [(if-not (zero? dx) (/ dx (abs dx)) 0)
     (if-not (zero? dy) (/ dy (abs dy)) 0)]))

(defn move-once
  [node direction]
  (let [deltas {:U [0 1], :D [0 -1], :L [-1 0], :R [1, 0]}]
    (add node (direction deltas))))

(defn tail-moves?
  [[hx hy] [tx ty]]
  (or (> (abs (- hx tx)) 1)
      (> (abs (- hy ty)) 1)))

(defn move-tail
  [head tail]
  (if (tail-moves? head tail)
    (add tail (delta head tail))
    tail))

(defn move-times
  [state times direction]
  (loop [i 0 state state]
    (if (< i times)
      (let [new-head (move-once (:head state) direction)
            new-tail (move-tail new-head (:tail state))
            visited (conj (:visited state) new-tail)]
        (recur (inc i) {:head new-head, :tail new-tail, :visited visited}))
      state)))

(defn part-1
  [input]
  (let [initial-state {:head [0 0]
                       :tail [0 0]
                       :visited #{[0 0]}}]
    (count (:visited
            (loop [state initial-state moves input]
              (if (first moves)
                (let [[dir cnt] (first moves)]
                  (recur (move-times state cnt dir) (rest moves)))
                state))))))

(part-1 test-input)
(part-1 (parse-input "../inputs/day_09.txt"))
