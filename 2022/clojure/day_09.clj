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

(defn move-segments
  [state direction]
  (let [{:keys [rope visited]} state
        new-rope (reduce (fn [head tail]
                           ((conj head (move-tail (peek head) tail))))
                         [(move-once (first rope) direction)]
                         (rest rope))]
    {:rope new-rope, :visited (conj visited (peek new-rope))}))

(defn move-rope
  [size instructions]
  (->> instructions
       (reduce
        (fn [state [direction times]]
          (nth (iterate #(move-segments % direction) state) times))
        {:rope (repeat size [0 0]), :visited #{[0 0]}})
       :visited
       count))

(defn part-1
  [input]
  (move-rope 2 input))

(defn part-2
  [input]
  (move-rope 10 input))

(def test-input
  (->> "R 4\nU 4\nL 3\nD 1\nR 4\nD 1\nL 5\nR 2"
       str/split-lines
       (map parse-move)))

(def test-input-2
  (->> "R 5\nU 8\nL 8\nD 3\nR 17\nD 10\nL 25\nU 20\n"
       str/split-lines
       (map parse-move)))

(part-1 test-input)
(part-1 (parse-input "../inputs/day_09.txt"))
(part-2 test-input-2)
(part-2 (parse-input "../inputs/day_09.txt"))