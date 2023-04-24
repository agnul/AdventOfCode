(ns day_09
  (:require [clojure.string :as str]))

(defn parse-move
  [string]
  (let [[direction cnt] (str/split string #"\s")]
    (list (keyword direction) (parse-long cnt))))

(defn parse-input
  [input]
  (->> input
       str/split-lines
       (map parse-move)))

(defn add
  [[x0 y0] [x1 y1]]
  [(+ x0 x1) (+ y0 y1)])

(defn sub
  [[x0 y0] [x1 y1]]
  [(- x0 x1) (- y0 y1)])

(defn delta
  [k1 k2]
  (let [[dx dy] (sub k1 k2)]
    [(if-not (zero? dx) (/ dx (abs dx)) 0)
     (if-not (zero? dy) (/ dy (abs dy)) 0)]))

(defn tail-moves?
  [[hx hy] [tx ty]]
  (or (> (abs (- hx tx)) 1)
      (> (abs (- hy ty)) 1)))

(defn move-knot
  [knot direction]
  (let [deltas {:U [0 1], :D [0 -1], :L [-1 0], :R [1, 0]}]
    (add knot (direction deltas))))

(defn move-tail
  [head tail]
  (if (tail-moves? head tail)
    (add tail (delta head tail))
    tail))

(defn move-rope
  [{:keys [rope visited]} direction]
  (let [moved (reduce
               (fn [head tail]
                 (conj head (move-tail (peek head) tail)))
               [(move-knot (first rope) direction)]
               (rest rope))]
    {:rope moved, :visited (conj visited (peek moved))}))

(defn solve
  [size instructions]
  (->> instructions
       (reduce
        (fn [state [direction times]]
          (nth (iterate #(move-rope % direction) state) times))
        {:rope (repeat size [0 0]), :visited #{[0 0]}})
       :visited
       count))

(defn part-1
  [input]
  (solve 2 input))

(defn part-2
  [input]
  (solve 10 input))

(def test-input
  (parse-input "R 4\nU 4\nL 3\nD 1\nR 4\nD 1\nL 5\nR 2"))

(def test-input-2
  (parse-input "R 5\nU 8\nL 8\nD 3\nR 17\nD 10\nL 25\nU 20\n"))

(part-1 test-input)
(part-1 (parse-input (slurp "../inputs/day_09.txt")))
(part-2 test-input-2)
(part-2 (parse-input (slurp "../inputs/day_09.txt")))
